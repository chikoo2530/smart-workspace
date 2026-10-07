from extensions import db
from datetime import datetime


class FacilityRequest(db.Model):
    __tablename__ = "facility_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    facility_type = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(500),
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Normal"
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="facility_requests"
    )