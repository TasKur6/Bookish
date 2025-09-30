from bookish.app import db

class Copy(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Copies'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, db.ForeignKey('Books.isbn', name='fk_book_isbn'), nullable=False)
    username = db.Column(db.String(), db.ForeignKey('Users.username', name='fk_copy_username'))
    due_back = db.Column(db.Date())

    def __init__(self, isbn):
        self.isbn = isbn

    def __repr__(self):
        return '<id {}, isbn {}, username {}, due_back {}>'.format(self.id, self.isbn, self.username, self.due_back)

    def serialize(self):
        return {
            'id': self.id,
            'isbn': self.isbn,
            'username': self.username,
            'due_back': self.due_back
        }
