from bookish.app import db


class User(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Users'

    # Here we outline what columns we want in our database
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<username {}, password {}>'.format(self.username, self.password)

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password
        }
