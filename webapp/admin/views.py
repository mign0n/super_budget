from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required
def admin_index():
    if current_user.is_admin:
        username = current_user.name
        title = f"Welcome {current_user.role} {username}!"
        return render_template('admin/admin.html', title=title)
    else:
        return redirect(url_for('index'))
