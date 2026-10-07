from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.parking import ParkingSlot
from models.visitor import Visitor


parking = Blueprint("parking", __name__)


@parking.route("/parking")
@login_required
def parking_dashboard():

    slots = ParkingSlot.query.order_by(
        ParkingSlot.floor,
        ParkingSlot.slot_number
    ).all()

    available_count = ParkingSlot.query.filter_by(
        status="Available"
    ).count()

    occupied_count = ParkingSlot.query.filter_by(
        status="Occupied"
    ).count()

    return render_template(
        "parking/dashboard.html",
        slots=slots,
        available_count=available_count,
        occupied_count=occupied_count
    )


@parking.route(
    "/parking/request/<int:visitor_id>",
    methods=["POST"]
)
@login_required
def request_parking(visitor_id):

    visitor = Visitor.query.filter_by(
        id=visitor_id,
        employee_id=current_user.id
    ).first_or_404()

    if not visitor.parking_required:

        flash(
            "This visitor does not require parking.",
            "warning"
        )

        return redirect(
            url_for("visitor.list_visitors")
        )

    available_slot = ParkingSlot.query.filter_by(
        status="Available"
    ).first()

    if not available_slot:

        flash(
            "No parking slots are currently available.",
            "danger"
        )

        return redirect(
            url_for("visitor.list_visitors")
        )

    available_slot.status = "Occupied"
    available_slot.vehicle_number = visitor.vehicle_number
    available_slot.visitor_id = visitor.id

    visitor.parking_slot = available_slot.slot_number
    visitor.parking_status = "Assigned"

    db.session.commit()

    flash(
        f"Parking slot {available_slot.slot_number} assigned.",
        "success"
    )

    return redirect(
        url_for("visitor.list_visitors")
    )


@parking.route(
    "/parking/release/<int:slot_id>",
    methods=["POST"]
)
@login_required
def release_parking(slot_id):

    slot = db.session.get(
        ParkingSlot,
        slot_id
    )

    if not slot:

        flash(
            "Parking slot not found.",
            "danger"
        )

        return redirect(
            url_for("parking.parking_dashboard")
        )

    visitor_id = slot.visitor_id

    if visitor_id:

        visitor = db.session.get(
            Visitor,
            visitor_id
        )

        if visitor:

            visitor.parking_slot = None
            visitor.parking_status = "Released"

    slot.status = "Available"
    slot.vehicle_number = None
    slot.visitor_id = None

    db.session.commit()

    flash(
        "Parking slot released.",
        "success"
    )

    return redirect(
        url_for("parking.parking_dashboard")
    )