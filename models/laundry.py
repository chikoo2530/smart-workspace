from extensions import db
from datetime import datetime


class LaundryRequest(db.Model):
    __tablename__ = "laundry_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    service_type = db.Column(
        db.String(50),
        nullable=False
    )

    items_count = db.Column(
        db.Integer,
        default=1
    )

    pickup_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Requested"
    )

    notes = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="laundry_requests"
    )