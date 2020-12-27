from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, login_required, logout_user

from webapp import app, login_manager
from webapp.forms import LoginForm
from webapp.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    username = current_user.name
    title = f"Welcome {username}!"
    return render_template('index.html', title=title)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Authorization"
    header = "Welcome to the Super Budget!"
    login_form = LoginForm()
    return render_template('login.html', title=title, header=header,
                           form=login_form,
                           )


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You are logged-in successfully.')
            return redirect(url_for('index'))
    flash('Invalid username or password.')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin_index():
    if current_user.is_admin:
        username = current_user.name
        title = f"Welcome {current_user.role} {username}!"
        return render_template('admin.html', title=title)
    else:
        return redirect(url_for('index'))
