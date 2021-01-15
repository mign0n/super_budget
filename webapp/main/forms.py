from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

# mock object
categories = ['Продукты', 'Транспорт', 'Дом', 'Развлечения', 'Прочее', 'Услуги', 'Зарплата']


class TransactionForm(FlaskForm):
    value = StringField(validators=[DataRequired()],
                        render_kw={"class": "form-control",
                                   "placeholder": "Money value"
                                   }
                        )
    date = DateField(validators=[DataRequired()],
                     format='%d.%m.%Y',
                     render_kw={"class": "form-control",
                                "placeholder": "dd.mm.yyyy"
                                }
                     )
    comment = StringField(render_kw={"class": "form-control",
                                     "placeholder": "Comment"
                                     }
                          )
    submit = SubmitField('Ok', render_kw={"class": "btn btn-primary"})
    is_income = SelectField(choices=[('', 'Expense'), (True, 'Income')],
                            coerce=bool,
                            render_kw={"class": "btn btn-primary dropdown-toggle",
                                       "data-toggle": "dropdown",
                                       "aria-haspopup": "true",
                                       "aria-expanded": "false"
                                       }
                            )
    category = SelectField(choices=categories,
                           render_kw={"class": "btn btn-primary dropdown-toggle",
                                      "data-toggle": "dropdown",
                                      "aria-haspopup": "true",
                                      "aria-expanded": "false"
                                      }
                           )
