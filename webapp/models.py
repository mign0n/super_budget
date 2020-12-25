from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(255), nullable=False, unique=True)
    role = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"<User: name = {self.name}, id = {self.id}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    name = db.Column(db.String(50), nullable=False, unique=True)
    is_income = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return (
            f"<Category: name = {self.name}, id = {self.id},"
            f" is_income = {self.is_income}>"
        )


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    is_actual = db.Column(db.Boolean, nullable=False)
    value = db.Column(db.DECIMAL, nullable=False)
    date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return (
            f"<Transaction: id = {self.id}, value = {self.value},"
            f"date = {self.date}, actual = {self.is_actual}>"
        )
