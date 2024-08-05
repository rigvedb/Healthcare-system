# scheduling_app/api.py
from flask import request, g, Blueprint, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from scheduling_app.models import Schedule, PatientProfile, Appointment, Post, Comment, db
from scheduling_app.auth import auth

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class ScheduleResource(Resource):
    def get(self):
        schedules = Schedule.query.all()
        return [schedule.serialize() for schedule in schedules]

    def post(self):
        new_schedule = Schedule(**request.get_json())
        db.session.add(new_schedule)
        db.session.commit()
        return new_schedule.serialize(), 201

    def delete(self, schedule_id):
        schedule = Schedule.query.get(schedule_id)
        if schedule:
            db.session.delete(schedule)
            db.session.commit()
            return '', 204
        return {'message': 'Schedule not found'}, 404

api.add_resource(ScheduleResource, '/schedules', '/schedules/<int:schedule_id>')

class PatientProfileAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        profile = PatientProfile.query.filter_by(user_id=user_id).first()
        if profile:
            return {
                'medical_history': profile.medical_history,
                'insurance_info': profile.insurance_info,
                'preferred_providers': profile.preferred_providers
            }
        return {'message': 'Profile not found'}, 404

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        profile = PatientProfile(user_id=user_id, **request.get_json())
        db.session.add(profile)
        db.session.commit()
        return {'message': 'Profile created successfully'}, 201

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        profile = PatientProfile.query.filter_by(user_id=user_id).first()
        if profile:
            for key, value in request.get_json().items():
                setattr(profile, key, value)
            db.session.commit()
            return {'message': 'Profile updated successfully'}, 200
        return {'message': 'Profile not found'}, 404

api.add_resource(PatientProfileAPI, '/patient/profile')

class AppointmentAPI(Resource):
    @jwt_required()
    def get(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            return appointment.serialize()
        return {'message': 'Appointment not found'}, 404

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        appointment = Appointment(patient_id=user_id, **request.get_json())
        db.session.add(appointment)
        db.session.commit()
        return {'message': 'Appointment created successfully'}, 201

    @jwt_required()
    def put(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            for key, value in request.get_json().items():
                setattr(appointment, key, value)
            db.session.commit()
            return {'message': 'Appointment updated successfully'}, 200
        return {'message': 'Appointment not found'}, 404

    @jwt_required()
    def delete(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
            return '', 204
        return {'message': 'Appointment not found'}, 404

api.add_resource(AppointmentAPI, '/appointments/<int:appointment_id>', '/appointments')

class PostResource(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if post:
                return post.serialize()
            return {'message': 'Post not found'}, 404
        else:
            posts = Post.query.all()
            return [post.serialize() for post in posts]

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        post = Post(user_id=user_id, **request.get_json())
        db.session.add(post)
        db.session.commit()
        return {'message': 'Post created successfully'}, 201

api.add_resource(PostResource, '/posts', '/posts/<int:post_id>')

class CommentResource(Resource):
    def get(self, post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return [comment.serialize() for comment in comments]

    @jwt_required()
    def post(self, post_id):
        user_id = get_jwt_identity()
        comment = Comment(user_id=user_id, post_id=post_id, **request.get_json())
        db.session.add(comment)
        db.session.commit()
        return {'message': 'Comment created successfully'}, 201

api.add_resource(CommentResource, '/posts/<int:post_id>/comments')
