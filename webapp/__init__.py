from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        title = "Welcome to the Super Budget!"
        return render_template('index.html', title=title)

    return app
