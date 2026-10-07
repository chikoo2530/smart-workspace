from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta

from extensions import db
from models.table import DiningTable, TableReservation


table = Blueprint("table", __name__)


# =========================================================
# TABLES
# =========================================================

@table.route("/tables")
@login_required
def tables():

    dining_tables = DiningTable.query.order_by(
        DiningTable.table_number
    ).all()

    return render_template(
        "table/tables.html",
        tables=dining_tables
    )


# =========================================================
# RESERVE TABLE
# =========================================================

@table.route(
    "/tables/reserve/<int:table_id>",
    methods=["POST"]
)
@login_required
def reserve_table(table_id):

    dining_table = db.session.get(
        DiningTable,
        table_id
    )

    if not dining_table:

        flash(
            "Table not found.",
            "danger"
        )

        return redirect(
            url_for("table.tables")
        )

    if dining_table.status != "Available":

        flash(
            "This table is currently unavailable.",
            "warning"
        )

        return redirect(
            url_for("table.tables")
        )

    reservation_date = request.form["reservation_date"]

    reservation_time = request.form["reservation_time"]

    guests = int(
        request.form["guests"]
    )

    reservation = TableReservation(

        user_id=current_user.id,

        table_id=dining_table.id,

        reservation_date=datetime.strptime(
            reservation_date,
            "%Y-%m-%d"
        ).date(),

        reservation_time=reservation_time,

        guests=guests,

        status="Confirmed"

    )

    dining_table.status = "Reserved"

    db.session.add(reservation)

    db.session.commit()

    flash(
        f"Table {dining_table.table_number} reserved successfully.",
        "success"
    )

    return redirect(
        url_for("table.my_reservations")
    )


# =========================================================
# MY RESERVATIONS
# =========================================================

@table.route("/tables/reservations")
@login_required
def my_reservations():

    reservations = TableReservation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        TableReservation.created_at.desc()
    ).all()

    # Convert UTC → IST
    for reservation in reservations:

        if reservation.created_at:

            reservation.ist_created_at = (
                reservation.created_at
                + timedelta(hours=5, minutes=30)
            )

    return render_template(
        "table/reservations.html",
        reservations=reservations
    )