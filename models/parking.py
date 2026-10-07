from extensions import db
from datetime import datetime


class ParkingSlot(db.Model):
    __tablename__ = "parking_slots"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    slot_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    floor = db.Column(
        db.String(20),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Available"
    )

    vehicle_number = db.Column(
        db.String(30),
        nullable=True
    )

    visitor_id = db.Column(
        db.Integer,
        db.ForeignKey("visitors.id"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )