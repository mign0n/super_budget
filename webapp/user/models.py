from flask_login import UserMixin
from webapp.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.String(5), nullable=False)

    categories = db.relationship('Category', backref='category_owner', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='transaction_owner', lazy='dynamic')

    def __repr__(self):
        return f"<User: name = {self.name}, id = {self.id}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'ADMIN'
