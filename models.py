from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def generate_auth_token(self):
        # Implement token generation logic here
        return 'example_token'

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80), nullable=False)
    event_description = db.Column(db.String(200), nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Schedule {self.event_name}>'

    def serialize(self):
        return {
            'id': self.id,
            'event_name': self.event_name,
            'event_description': self.event_description,
            'event_date': self.event_date.strftime('%Y-%m-%d %H:%M:%S')
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')), onupdate=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.content}>'

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Doctor('{self.name}')"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Patient('{self.name}')"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))

    def __repr__(self):
        return f"Appointment('{self.appointment_datetime}', '{self.doctor_id}', '{self.patient_id}')"
    
    def serialize(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'patient_id': self.patient_id,
            'appointment_datetime': self.appointment_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'reason': self.reason,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)
    treatment = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    patient = db.relationship('Patient', backref=db.backref('medical_records', lazy=True))

    def __repr__(self):
        return f"MedicalRecord('{self.diagnosis}', '{self.treatment}')"

    def serialize(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medical_history = db.Column(db.String(200), nullable=True)
    insurance_info = db.Column(db.String(200), nullable=True)
    preferred_providers = db.Column(db.String(200), nullable=True)
    user = db.relationship('User', backref=db.backref('patient_profile', uselist=False))

    def __repr__(self):
        return f"PatientProfile('{self.user_id}', '{self.medical_history}', '{self.insurance_info}', '{self.preferred_providers}')"

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'medical_history': self.medical_history,
            'insurance_info': self.insurance_info,
            'preferred_providers': self.preferred_providers
        }
