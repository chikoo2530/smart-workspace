from flask import Blueprint, render_template
from flask_login import login_required


security = Blueprint("security", __name__, url_prefix="/security")


@security.route("/dashboard")
@login_required
def dashboard():
    return render_template("security/dashboard.html")