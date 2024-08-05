from marshmallow import Schema, fields, validate

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    doctor_id = fields.Int(required=True)
    patient_id = fields.Int(required=True)
    appointment_datetime = fields.DateTime(required=True)
    reason = fields.Str(required=True, validate=validate.Length(max=200))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
