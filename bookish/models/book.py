from bookish.app import db


class Book(db.Model):
    __tablename__ = 'Books'

    isbn = db.Column(db.String(17), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    copies = db.relationship('Copy', backref='book', lazy='dynamic')

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author

    def __repr__(self):
        return '<isbn {}, title {}, author {}, copies_total {}>'.format(self.isbn, self.title, self.author, self.copies_total)

    @property
    def copies_available(self):
        return self.copies.filter_by(username=None).count()

    def serialize(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'copies_total': self.copies_total,
            'copies_available': self.copies_available
        }

    @property
    def copies_total(self):
        return self.copies.count()
