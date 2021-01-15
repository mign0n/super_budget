from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from webapp import db
from webapp.user.models import User
from webapp.main.models import Category, Transaction
from webapp.main.forms import TransactionForm

bp = Blueprint('main', __name__, url_prefix=None)


@bp.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('user.login'))
    username = current_user.name
    title = f"Welcome {username}!"
    form = TransactionForm()
    return render_template('main/index.html', title=title, form=form)


@bp.route('/transaction', methods=['POST'])
def transaction():
    form = TransactionForm()

    user = User.query.filter_by(name=current_user.name).first()

    is_income = form.is_income.data
    category_name = form.category.data
    category = Category.query.filter_by(name=category_name, is_income=is_income).first()

    # mock object
    is_actual = True
    value = form.value.data
    date = form.date.data
    comment = form.comment.data
    new_transaction = Transaction(is_actual=is_actual,
                                  value=value,
                                  date=date,
                                  comment=comment,
                                  trans_cat=category,
                                  transaction_owner=user)

    db.session.add(new_transaction)
    db.session.commit()

    flash(f"Data was write successfully. "
          f"Is income: {is_income}; money: {value}; "
          f"category: {category}; date: {date}; {comment}")
    return redirect(url_for('main.index'))
