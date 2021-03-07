from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.db import db
from webapp.admin.views import bp as admin_bp
from webapp.main.views import bp as main_bp
from webapp.user.models import User
from webapp.main.models import Category, Transaction
from webapp.user.views import bp as user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app


app = create_app()
