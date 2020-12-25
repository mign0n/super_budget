from flask import Flask
from flask_login import LoginManager
from webapp.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    return app, login_manager


app, login_manager = create_app()


from webapp import views
