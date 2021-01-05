from getpass import getpass
import sys

from webapp import create_app
from webapp.db import User, db

app, _ = create_app()

with app.app_context():
    username = input('Enter username: ')
    if User.query.filter(User.name == username).count():
        print('This user already exists.')
        sys.exit(0)

    role = input('Choice your role. (ADMIN or USER) ').upper()
    email = input('Enter email address: ')
    password = getpass('Enter password: ')
    password2 = getpass('Re-type password: ')
    if not password == password2:
        sys.exit(0)

    new_user = User(name=username, email=email, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print(f"User with id={new_user.id} added.")
