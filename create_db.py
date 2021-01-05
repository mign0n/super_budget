from webapp import db, create_app


app, _ = create_app()
db.create_all(app=app)
