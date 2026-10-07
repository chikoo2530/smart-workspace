from extensions import db
from datetime import datetime


class Visitor(db.Model):
    __tablename__ = "visitors"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    visitor_name = db.Column(
        db.String(100),
        nullable=False
    )

    visitor_phone = db.Column(
        db.String(20),
        nullable=False
    )

    visit_date = db.Column(
        db.Date,
        nullable=False
    )

    vehicle_number = db.Column(
        db.String(30),
        nullable=True
    )

    parking_required = db.Column(
        db.Boolean,
        default=False
    )

    parking_slot = db.Column(
        db.String(20),
        nullable=True
    )

    parking_status = db.Column(
        db.String(20),
        default="Not Required"
    )

    qr_token = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    employee = db.relationship(
        "User",
        backref="visitors"
    )