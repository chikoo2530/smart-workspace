from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from extensions import db
from models.laundry import LaundryRequest


laundry = Blueprint("laundry", __name__)


@laundry.route("/laundry")
@login_required
def laundry_dashboard():

    requests = LaundryRequest.query.filter_by(
        user_id=current_user.id
    ).order_by(
        LaundryRequest.created_at.desc()
    ).all()

    return render_template(
        "laundry/dashboard.html",
        requests=requests
    )


@laundry.route(
    "/laundry/request",
    methods=["POST"]
)
@login_required
def create_request():

    service_type = request.form[
        "service_type"
    ]

    items_count = int(
        request.form["items_count"]
    )

    pickup_date = request.form[
        "pickup_date"
    ]

    notes = request.form.get(
        "notes",
        ""
    ).strip()

    laundry_request = LaundryRequest(
        user_id=current_user.id,
        service_type=service_type,
        items_count=items_count,
        pickup_date=datetime.strptime(
            pickup_date,
            "%Y-%m-%d"
        ).date(),
        status="Requested",
        notes=notes or None
    )

    db.session.add(laundry_request)
    db.session.commit()

    flash(
        "Laundry request submitted successfully.",
        "success"
    )

    return redirect(
        url_for("laundry.laundry_dashboard")
    )