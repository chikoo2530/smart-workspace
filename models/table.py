from extensions import db
from datetime import datetime


class DiningTable(db.Model):
    __tablename__ = "dining_tables"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    table_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    capacity = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Available"
    )


class TableReservation(db.Model):
    __tablename__ = "table_reservations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    table_id = db.Column(
        db.Integer,
        db.ForeignKey("dining_tables.id"),
        nullable=False
    )

    reservation_date = db.Column(
        db.Date,
        nullable=False
    )

    reservation_time = db.Column(
        db.String(20),
        nullable=False
    )

    guests = db.Column(
        db.Integer,
        default=1
    )

    status = db.Column(
        db.String(20),
        default="Confirmed"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="table_reservations"
    )

    table = db.relationship(
        "DiningTable",
        backref="reservations"
    )