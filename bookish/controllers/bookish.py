from flask import request
from bookish.models.book import Book
from bookish.models.copy import Copy
from bookish.models.user import User
from bookish.models import db


def bookish_routes(app):
    @app.route('/healthcheck')
    def health_check():
        return {"status": "OK"}

    @app.route('/book', methods=['POST', 'GET'])
    def handle_book():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_book = Book(isbn=data['isbn'], title=data['title'], author=data['author'], copies_total=data['copies_total'])
                db.session.add(new_book)
                db.session.commit()
                return {"message": "New book has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            books = Book.query.all()
            results = [
                {
                    'isbn': book.isbn,
                    'title': book.title,
                    'author': book.author,
                    'copies_total': book.copies_total,
                    'copies_available': book.copies_available
                } for book in books]
            return {"books": results}

    @app.route('/copy', methods=['POST', 'GET'])
    def handle_copy():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_copy = Copy(isbn=data['isbn'])
                db.session.add(new_copy)
                db.session.commit()
                return {"message": "New copy has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            copies = Copy.query.all()
            results = [
                {
                    'id': copy.id,
                    'isbn': copy.isbn
                } for copy in copies]
            return {"copies": results}

    @app.route('/user', methods=['POST', 'GET'])
    def handle_user():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_user = User(username=data['username'], password=data['password'])
                db.session.add(new_user)
                db.session.commit()
                return {"message": "New user has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            users = User.query.all()
            results = [
                {
                    'username': user.username,
                    'password': user.password
                } for user in users]
            return {"users": results}
