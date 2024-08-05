# scheduling_app/seed.py

from datetime import datetime
import pytz
from scheduling_app.models import db, Schedule
from scheduling_app.app import app

with app.app_context():
    db.create_all()

    # Add some seed data
    new_schedule = Schedule(
        event_name="Team Meeting",
        event_description="Weekly team sync",
        event_date=datetime.now(pytz.timezone('Asia/Kolkata'))
    )

    db.session.add(new_schedule)
    db.session.commit()
    print("Database seeded.")

