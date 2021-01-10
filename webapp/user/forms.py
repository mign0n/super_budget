from flask_wtf import FlaskForm
<<<<<<< Updated upstream
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
=======
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
>>>>>>> Stashed changes

from webapp.user.models import User

class LoginForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Enter username",
                                      }
                           )

    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"class": "form-control",
                                        "placeholder": "Enter password",
                                        "type": "password",
                                        }
<<<<<<< Updated upstream
                             )
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})
=======
                            )
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary"})

    remember_me = BooleanField('Запомнить меня!', default=True, 
                                render_kw={"class": "form-check-input"})


class RegistrationForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired(),],
                            render_kw={"class": "form-control",
                                        "placeholder": "Enter username"
                                        }
                           )
    email = StringField('Email', validators=[DataRequired(), Email()],
                            render_kw={"class": "form-control",
                                       "placeholder": "Enter email"
                                       }
                        )
    password = PasswordField('Password', validators=[DataRequired()], 
                            render_kw={"class": "form-control",
                                        "placeholder": "Enter password",
                                        "type": "password"
                                        }
                             )
    password2 = PasswordField('Confirm password',
                            validators=[DataRequired(), EqualTo('password')],
                            render_kw={"class": "form-control",
                                        "placeholder": "Enter password",
                                        "type": "password"
                                        }
                              )
    submit = SubmitField('Register!', render_kw={"class": "btn btn-primary"})


    def validate_username(self, name):
        users_count = User.query.filter_by(name=name.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')

    def validate_email(self, email):
        users_coutn = User.query.filter_by(email=email.data).count()
        if users_coutn > 0:
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован')
>>>>>>> Stashed changes
