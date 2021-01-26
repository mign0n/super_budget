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

    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary"})

    remember_me = BooleanField('Запомнить меня!', default=True,
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

    submit = SubmitField('Register!', render_kw={"class": "btn btn-primary"})

    def validate_username(self, name):
        user_exist = db.session.query(exists().where(User.name == name.data)).scalar()
        if user_exist:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

    def validate_email(self, email):
        user_exist = db.session.query(exists().where(User.email == email.data)).scalar()
        if user_exist:
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован')


class CategoryForm(FlaskForm):
    new_category = StringField('Новая категория', validators=[DataRequired()],
                               render_kw={"class": "form-control",
                                          "placeholder": "Название категории"})

    is_income = SelectField('Тип категории', choices=[('1', 'Доход'), ('0', 'Расход')],
                            render_kw={"class": "form-select",
                                       "aria-label": "Default select example"})

    submit = SubmitField('Добавить', render_kw={"class": "btn btn-primary"})

    def validate_new_category(self, new_category):
        category_exist = db.session.query(exists().where(
            and_(Category.name == new_category.data, Category.user_id == current_user.id)
        )).scalar()
        if category_exist:
            raise ValidationError('У вас уже есть такая категория!')
