from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from webapp import db
from webapp.main.models import Category, Transaction
from webapp.main.forms import TransactionForm
from webapp.user.forms import CategoryForm

bp = Blueprint('main', __name__, url_prefix=None)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    username = current_user.name
    title = f"Welcome {username}!"
    available_categories = db.session.query(Category).filter(
        or_(Category.user_id == current_user.id, Category.user_id.is_(None))
    ).all()
    categories_list = [(ac.id, ac.name) for ac in available_categories]

    form = TransactionForm()
    form.category.choices = categories_list

    if form.validate_on_submit():
        is_income = form.is_income.data
        category_id = form.category.data
        category = Category.query.filter_by(id=category_id, is_income=is_income).first()

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
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: {error}')
    return render_template('main/index.html', title=title, form=form)


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
