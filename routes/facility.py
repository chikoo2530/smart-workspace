from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.facility import FacilityRequest


facility = Blueprint("facility", __name__)


@facility.route("/facilities")
@login_required
def facility_dashboard():

    requests = FacilityRequest.query.filter_by(
        user_id=current_user.id
    ).order_by(
        FacilityRequest.created_at.desc()
    ).all()

    return render_template(
        "facility/dashboard.html",
        requests=requests
    )


@facility.route(
    "/facilities/request",
    methods=["POST"]
)
@login_required
def create_request():

    facility_type = request.form[
        "facility_type"
    ]

    description = request.form[
        "description"
    ].strip()

    priority = request.form.get(
        "priority",
        "Normal"
    )

    if not description:

        flash(
            "Please enter a description.",
            "warning"
        )

        return redirect(
            url_for(
                "facility.facility_dashboard"
            )
        )

    facility_request = FacilityRequest(
        user_id=current_user.id,
        facility_type=facility_type,
        description=description,
        priority=priority,
        status="Pending"
    )

    db.session.add(facility_request)
    db.session.commit()

    flash(
        "Facility request submitted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "facility.facility_dashboard"
        )
    )