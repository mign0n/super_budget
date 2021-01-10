from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp import db


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    title = "Authorization"
    header = "Welcome to the Super Budget!"
    login_form = LoginForm()
    return render_template('user/login.html', title=title, header=header,
                           form=login_form,
                           )


@bp.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You are logged-in successfully.')
            return redirect(url_for('main.index'))
    flash('Invalid username or password.')
    return redirect(url_for('user.login'))


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@bp.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    title = "Registration"
    form = RegistrationForm()
    return render_template('user/register.html', title=title, form=form)


@bp.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(name=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: {error}')
        return redirect(url_for('user.register'))