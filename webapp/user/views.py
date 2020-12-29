from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm
from webapp.user.models import User


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    title = "Authorization"
    header = "Welcome to the Super Budget!"
    login_form = LoginForm()
    return render_template('login.html', title=title, header=header,
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
