from flask import render_template
from webapp import app


@app.route('/')
def index():
    title = "Welcome to the Super Budget!"
    return render_template('index.html', title=title)
