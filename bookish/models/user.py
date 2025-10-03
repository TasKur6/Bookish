from bookish.app import db


class User(db.Model):
    __tablename__ = 'Users'

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(128), nullable=False)

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
