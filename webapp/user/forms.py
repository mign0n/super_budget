from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy.sql import and_, exists
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.db import db
from webapp.main.models import Category
from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Enter username"})

    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"class": "form-control",
                                        "placeholder": "Enter password",
                                        "type": "password"})

    submit = SubmitField('Log-In', render_kw={"class": "btn btn-primary"})

    remember_me = BooleanField('Remember me', default=False,
                               render_kw={"class": "form-check-input"})


class RegistrationForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Enter username"})

    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control",
                                   "placeholder": "Enter email"})

    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"class": "form-control",
                                        "placeholder": "Enter password",
                                        "type": "password"})

    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control",
                                         "placeholder": "Enter password",
                                         "type": "password"})

    submit = SubmitField('Register', render_kw={"class": "btn btn-primary"})

    def validate_username(self, name):
        user_exist = db.session.query(exists().where(User.name == name.data)).scalar()
        if user_exist:
            raise ValidationError('A user with this name is already registered.')

    def validate_email(self, email):
        user_exist = db.session.query(exists().where(User.email == email.data)).scalar()
        if user_exist:
            raise ValidationError('A user with this email is already registered.')


class CategoryForm(FlaskForm):
    new_category = StringField('New category', validators=[DataRequired()],
                               render_kw={"class": "form-control",
                                          "placeholder": "Category name"})

    is_income = SelectField('Category type', choices=[('1', 'Income'), ('0', 'Expense')],
                            render_kw={"class": "form-select",
                                       "aria-label": "Default select example"})

    submit = SubmitField('Add', render_kw={"class": "btn btn-primary"})

    def validate_new_category(self, new_category):
        category_exist = db.session.query(exists().where(
            and_(Category.name == new_category.data, Category.user_id == current_user.id)
        )).scalar()
        if category_exist:
            raise ValidationError('You already have this category.')
