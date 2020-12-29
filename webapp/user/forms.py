from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Enter username",
                                      }
                           )
    email = StringField('Email address', validators=[DataRequired()],
                        render_kw={"class": "form-control",
                                   "placeholder": "Enter email",
                                   "type": "email",
                                   }
                        )
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"class": "form-control",
                                        "placeholder": "Enter password",
                                        "type": "password",
                                        }
                             )
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})
