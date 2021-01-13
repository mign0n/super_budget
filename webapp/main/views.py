from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

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
    is_income = form.is_income.data
    value = form.value.data
    category = form.category.data
    date = form.date.data
    comment = form.comment.data

    flash(f"Data was write successfully. "
          f"Is income: {is_income}; money: {value}; "
          f"category: {category}; date: {date}; {comment}")
    return redirect(url_for('main.index'))
