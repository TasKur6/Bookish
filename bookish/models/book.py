from bookish.app import db


class Book(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Books'

    # Here we outline what columns we want in our database
    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    copies_total = db.Column(db.Integer)
    copies_available = db.Column(db.Integer)

    def __init__(self, isbn, title, author, copies_total):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.copies_total = copies_total
        self.copies_available = copies_total

    def __repr__(self):
        return '<isbn {}, title {}, author {}, copies {}>'.format(self.isbn, self.title, self.author, self.copies)

    def serialize(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'copies_total': self.copies_total,
            'copies_available': self.copies_available
        }
