from flask import Blueprint, render_template
from flask_login import login_required

from models.user import User
from models.visitor import Visitor
from models.parking import ParkingSlot
from models.food import FoodOrder
from models.table import TableReservation
from models.laundry import LaundryRequest
from models.facility import FacilityRequest


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/dashboard")
@login_required
def dashboard():

    users = User.query.count()
    visitors = Visitor.query.count()
    parking_total = ParkingSlot.query.count()
    parking_occupied = ParkingSlot.query.filter_by(
        status="Occupied"
    ).count()
    food_orders = FoodOrder.query.count()
    reservations = TableReservation.query.count()
    laundry_requests = LaundryRequest.query.count()
    facility_requests = FacilityRequest.query.count()

    return render_template(
        "admin/dashboard.html",
        users=users,
        visitors=visitors,
        parking_total=parking_total,
        parking_occupied=parking_occupied,
        food_orders=food_orders,
        reservations=reservations,
        laundry_requests=laundry_requests,
        facility_requests=facility_requests
    )