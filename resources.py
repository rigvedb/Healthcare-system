# scheduling_app/resources.py

from flask_restful import Resource, reqparse
from scheduling_app.models import Schedule, db

class ScheduleResource(Resource):
    def get(self, schedule_id=None):
        if schedule_id:
            schedule = Schedule.query.get(schedule_id)
            if schedule:
                return schedule.serialize()
            return {'message': 'Schedule not found'}, 404
        else:
            schedules = Schedule.query.all()
            return [schedule.serialize() for schedule in schedules]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', required=True)
        parser.add_argument('event_description', required=True)
        parser.add_argument('event_date', required=True)
        args = parser.parse_args()
        
        schedule = Schedule(
            event_name=args['event_name'],
            event_description=args['event_description'],
            event_date=args['event_date']
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule.serialize(), 201

    def put(self, schedule_id):
        parser = reqparse.RequestParser()
        parser.add_argument('event_name', required=True)
        parser.add_argument('event_description', required=True)
        parser.add_argument('event_date', required=True)
        args = parser.parse_args()
        
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return {'message': 'Schedule not found'}, 404
        
        schedule.event_name = args['event_name']
        schedule.event_description = args['event_description']
        schedule.event_date = args['event_date']
        db.session.commit()
        return schedule.serialize()

    def delete(self, schedule_id):
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            return {'message': 'Schedule not found'}, 404
        
        db.session.delete(schedule)
        db.session.commit()
        return {'message': 'Schedule deleted'}, 200
