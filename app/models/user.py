from app.extensions import db
from flask_login import UserMixin
from passlib.hash import scrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Store the scrypt hash
    role = db.Column(db.String(20), default='contributor')

    def set_password(self, password):
        self.password_hash = scrypt.hash(password)

    def check_password(self, password):
        try:
            return scrypt.verify(password, self.password_hash)
        except ValueError:  # Handle incorrect hash format
            return False

    def __repr__(self):
        return f'<User {self.username}>'