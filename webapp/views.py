from flask import render_template
from webapp import app
from webapp.forms import LoginForm


@app.route('/')
def index():
    title = "Welcome to the Super Budget!"
    return render_template('index.html', title=title)


@app.route('/login')
def login():
    title = "Authorization"
    login_form = LoginForm()
    return render_template('login.html', title=title, form=login_form)
