from bookish.app import db

class Copy(db.Model):
    __tablename__ = 'Copies'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(17), db.ForeignKey('Books.isbn', name='fk_book_isbn', ondelete='CASCADE'), nullable=False, index=True)
    username = db.Column(db.String(50), db.ForeignKey('Users.username', name='fk_copy_username', ondelete='SET NULL'), nullable=True, index=True)
    due_back = db.Column(db.Date(), nullable=True)

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
