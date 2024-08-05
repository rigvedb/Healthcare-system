from flask import Blueprint, request, jsonify
from . import db
from .models import Appointment, AppointmentSchema

appointments = Blueprint('appointments', __name__)
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

@appointments.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    errors = appointment_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    appointment = Appointment(
        doctor_id=data['doctor_id'],
        patient_id=data['patient_id'],
        appointment_datetime=data['appointment_datetime'],
        reason=data['reason']
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment_schema.jsonify(appointment), 201

@appointments.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return appointments_schema.jsonify(appointments), 200

@appointments.route('/appointments/<int:id>', methods=['GET'])
def get_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return appointment_schema.jsonify(appointment), 200

@appointments.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    data = request.get_json()
    errors = appointment_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    appointment.doctor_id = data['doctor_id']
    appointment.patient_id = data['patient_id']
    appointment.appointment_datetime = data['appointment_datetime']
    appointment.reason = data['reason']
    db.session.commit()
    return appointment_schema.jsonify(appointment), 200

@appointments.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return '', 204
