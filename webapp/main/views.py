from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from webapp import db
from webapp.main.models import Category, Transaction
from webapp.main.forms import TransactionForm
from webapp.user.forms import CategoryForm

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
                                  transaction_owner=current_user)

    db.session.add(new_transaction)
    db.session.commit()

    flash(f"Data has been written successfully. "
          f"Is income: {is_income}; money: {value}; "
          f"category: {category.name}; date: {date}; {comment}")
    return redirect(url_for('main.index'))


@bp.route('/category_adding')
def category_adding():
    title = "Add new category"
    form = CategoryForm()
    return render_template('main/category_adding.html', title=title, form=form)


@bp.route('/category_adding-process', methods=['POST'])
def category_adding_process():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(user_id=current_user.id,
                                name=form.new_category.data,
                                is_income=bool(int(form.is_income.data)))
        db.session.add(new_category)
        db.session.commit()
        flash('Категория успешно добавлена!')
        return redirect(url_for('main.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: {error}')
        return redirect(url_for('main.category_adding'))
