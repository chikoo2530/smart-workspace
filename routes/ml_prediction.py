from flask import Blueprint, render_template, request
from flask_login import login_required

from ml.parking_model import predict_parking


ml_prediction = Blueprint(
    "ml_prediction",
    __name__,
    url_prefix="/ml"
)


@ml_prediction.route("/parking", methods=["GET", "POST"])
@login_required
def parking_prediction():

    result = None

    if request.method == "POST":

        hour = int(request.form["hour"])
        day = int(request.form["day"])
        visitors = int(request.form["visitors"])
        employees = int(request.form["employees"])
        previous_occupancy = int(
            request.form["previous_occupancy"]
        )

        result = predict_parking(
            hour,
            day,
            visitors,
            employees,
            previous_occupancy
        )

    return render_template(
        "ml_parking.html",
        result=result
    )