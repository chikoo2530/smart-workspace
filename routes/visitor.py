from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
import secrets

from extensions import db
from models.visitor import Visitor
from models.parking import ParkingSlot


visitor = Blueprint("visitor", __name__)


# =========================================================
# VISITOR LIST
# =========================================================

@visitor.route("/visitors")
@login_required
def list_visitors():

    visitors = Visitor.query.filter_by(
        employee_id=current_user.id
    ).order_by(
        Visitor.created_at.desc()
    ).all()

    return render_template(
        "visitor/list.html",
        visitors=visitors
    )


# =========================================================
# ADD VISITOR
# =========================================================

@visitor.route("/visitors/add", methods=["GET", "POST"])
@login_required
def add_visitor():

    if request.method == "POST":

        visitor_name = request.form[
            "visitor_name"
        ].strip()

        visitor_phone = request.form[
            "visitor_phone"
        ].strip()

        visit_date = request.form[
            "visit_date"
        ]

        vehicle_number = request.form.get(
            "vehicle_number",
            ""
        ).strip()

        parking_required = (
            request.form.get("parking_required")
            == "yes"
        )


        # -----------------------------------------
        # Convert date
        # -----------------------------------------

        visitor_date = datetime.strptime(
            visit_date,
            "%Y-%m-%d"
        ).date()


        # -----------------------------------------
        # Generate QR token
        # -----------------------------------------

        qr_token = secrets.token_urlsafe(32)


        # -----------------------------------------
        # Create Visitor
        # -----------------------------------------

        new_visitor = Visitor(

            employee_id=current_user.id,

            visitor_name=visitor_name,

            visitor_phone=visitor_phone,

            visit_date=visitor_date,

            vehicle_number=(
                vehicle_number
                if vehicle_number
                else None
            ),

            parking_required=parking_required,

            parking_status=(
                "Required"
                if parking_required
                else "Not Required"
            ),

            status="Pending",

            qr_token=qr_token
        )


        db.session.add(new_visitor)

        db.session.flush()


        # -----------------------------------------
        # AUTOMATIC PARKING ASSIGNMENT
        # -----------------------------------------

        if parking_required:

            if not vehicle_number:

                db.session.rollback()

                flash(
                    "Please enter vehicle number when parking is required.",
                    "warning"
                )

                return redirect(
                    url_for("visitor.add_visitor")
                )


            available_slot = ParkingSlot.query.filter_by(
                status="Available"
            ).order_by(
                ParkingSlot.floor,
                ParkingSlot.slot_number
            ).first()


            # No parking available
            if not available_slot:

                db.session.rollback()

                flash(
                    "No parking slots are currently available.",
                    "danger"
                )

                return redirect(
                    url_for("visitor.add_visitor")
                )


            # -------------------------------------
            # BOOK PARKING SLOT
            # -------------------------------------

            available_slot.status = "Occupied"

            available_slot.vehicle_number = (
                vehicle_number
            )

            available_slot.visitor_id = (
                new_visitor.id
            )


            new_visitor.parking_slot = (
                available_slot.slot_number
            )

            new_visitor.parking_status = (
                "Assigned"
            )


        # -----------------------------------------
        # Save everything
        # -----------------------------------------

        db.session.commit()


        flash(
            "Visitor added successfully.",
            "success"
        )


        # -----------------------------------------
        # Go directly to QR
        # -----------------------------------------

        return redirect(
            url_for(
                "visitor.visitor_qr",
                visitor_id=new_visitor.id
            )
        )


    return render_template(
        "visitor/add.html"
    )


# =========================================================
# VISITOR QR
# =========================================================

@visitor.route(
    "/visitors/<int:visitor_id>/qr"
)
@login_required
def visitor_qr(visitor_id):

    visitor_data = Visitor.query.filter_by(
        id=visitor_id,
        employee_id=current_user.id
    ).first_or_404()

    return render_template(
        "visitor/qr.html",
        visitor=visitor_data
    )


# =========================================================
# VERIFY VISITOR QR
# =========================================================

@visitor.route(
    "/visitor/verify/<qr_token>"
)
def verify_visitor(qr_token):

    visitor_data = Visitor.query.filter_by(
        qr_token=qr_token
    ).first()


    if not visitor_data:

        return render_template(
            "visitor/verify.html",
            visitor=None
        )


    return render_template(
        "visitor/verify.html",
        visitor=visitor_data
    )


# =========================================================
# APPROVE VISITOR
# =========================================================

@visitor.route(
    "/visitors/<int:visitor_id>/approve",
    methods=["POST"]
)
@login_required
def approve_visitor(visitor_id):

    visitor_data = Visitor.query.filter_by(
        id=visitor_id,
        employee_id=current_user.id
    ).first_or_404()


    visitor_data.status = "Approved"

    db.session.commit()


    flash(
        "Visitor approved successfully.",
        "success"
    )


    return redirect(
        url_for("visitor.list_visitors")
    )