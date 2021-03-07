from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from webapp.admin.views import bp as admin_bp
from webapp.diagram.dashboard import init_dashboard
from webapp.db import db
from webapp.main.models import Category, Transaction
from webapp.main.views import bp as main_bp
from webapp.user.models import User
from webapp.user.views import bp as user_bp


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile('config.py')
    db.init_app(flask_app)
    migrate = Migrate(flask_app, db, render_as_batch=True)

    login_manager = LoginManager()
    login_manager.init_app(flask_app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(user_bp)

    application = init_dashboard(flask_app)

    return application


app = create_app()
