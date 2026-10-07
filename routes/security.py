from flask import Blueprint, render_template
from flask_login import login_required

from models.visitor import Visitor


security = Blueprint(
    "security",
    __name__,
    url_prefix="/security"
)


@security.route("/dashboard")
@login_required
def dashboard():

    pending_visitors = Visitor.query.order_by(
        Visitor.created_at.desc()
    ).all()

    return render_template(
        "security/dashboard.html",
        visitors=pending_visitors
    )