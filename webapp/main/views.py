from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user


bp = Blueprint('main', __name__, url_prefix=None)


@bp.route('/')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('user.login'))
    username = current_user.name
    title = f"Welcome {username}!"
    return render_template('main/index.html', title=title)
