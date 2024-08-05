# scheduling_app/create_db.py
from scheduling_app.app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
