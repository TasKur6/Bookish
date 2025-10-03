from flask import request
from bookish.models.book import Book
from bookish.models.copy import Copy
from bookish.models.user import User
from bookish.models import db
from sqlalchemy.exc import IntegrityError


def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

    @app.route('/book', methods=['POST', 'GET'])
    def handle_book():
        if request.method == 'POST':
            if not request.is_json:
                return {"error": "The request payload is not in JSON format"}, 400

            data = request.get_json()

            required = ['isbn', 'title', 'author']
            missing = [f for f in required if f not in data]
            if missing:
                return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

            if not isinstance(data.get('isbn'), str) or not isinstance(data.get('title'), str) or not isinstance(data.get('author'), str):
                return {"error": "Fields 'isbn', 'title' and 'author' must be strings."}, 400

            copies_count = data.get('copies_total')
            if copies_count is not None:
                if not (isinstance(copies_count, int) and copies_count >= 0):
                    return {"error": "'copies_total' must be a non-negative integer if provided."}, 400

            new_book = Book(isbn=data['isbn'], title=data['title'], author=data['author'])
            try:
                db.session.add(new_book)
                db.session.flush()

                if copies_count:
                    for _ in range(copies_count):
                        db.session.add(Copy(isbn=new_book.isbn))

                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                return {"error": "Database integrity error - maybe the ISBN already exists in the database."}, 409

            return {"message": "New book has been created successfully.", "isbn": new_book.isbn}, 200

        elif request.method == 'GET':
            books = Book.query.all()
            results = [book.serialize() for book in books]
            return {"books": results}

    @app.route('/copy', methods=['POST', 'GET'])
    def handle_copy():
        if request.method == 'POST':
            if not request.is_json:
                return {"error": "The request payload is not in JSON format"}, 400

            data = request.get_json()
            if 'isbn' not in data:
                return {"error": "Missing required field: isbn"}, 400
            if not isinstance(data.get('isbn'), str):
                return {"error": "Field 'isbn' must be a string."}, 400

            new_copy = Copy(isbn=data['isbn'])
            try:
                db.session.add(new_copy)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return {"error": "Database integrity error - maybe the referenced book does not exist or duplicate copy id."}, 409

            return {"message": "New copy has been created successfully.", "id": new_copy.id}, 201

        elif request.method == 'GET':
            copies = Copy.query.all()
            results = [copy.serialize() for copy in copies]
            return {"copies": results}

    @app.route('/user', methods=['POST', 'GET'])
    def handle_user():
        if request.method == 'POST':
            if not request.is_json:
                return {"error": "The request payload is not in JSON format"}, 400

            data = request.get_json()
            required = ['username', 'password']
            missing = [f for f in required if f not in data]
            if missing:
                return {"error": f"Missing required fields: {', '.join(missing)}"}, 400
            if not isinstance(data.get('username'), str) or not isinstance(data.get('password'), str):
                return {"error": "Fields 'username' and 'password' must be strings."}, 400

            new_user = User(username=data['username'], password=data['password'])
            try:
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return {"error": "Database integrity error - username may already exist."}, 409

            return {"message": "New user has been created successfully.", "username": new_user.username}, 201

        elif request.method == 'GET':
            users = User.query.all()
            results = [user.serialize() for user in users]
            return {"users": results}
