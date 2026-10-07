from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from models.visitor import Visitor
from models.parking import ParkingSlot
from models.food import MenuItem, FoodOrder
from models.table import TableReservation
from models.laundry import LaundryRequest
from models.facility import FacilityRequest


ai_assistant = Blueprint(
    "ai_assistant",
    __name__,
    url_prefix="/ai-assistant"
)


@ai_assistant.route("/", methods=["GET", "POST"])
@login_required
def assistant():

    answer = None
    question = ""

    if request.method == "POST":

        question = request.form.get("question", "").strip().lower()

        if any(word in question for word in ["parking", "park", "vehicle"]):

            available = ParkingSlot.query.filter_by(
                status="Available"
            ).count()

            occupied = ParkingSlot.query.filter_by(
                status="Occupied"
            ).count()

            answer = (
                f"Smart Parking: {available} slots are currently "
                f"available and {occupied} slots are occupied. "
                "You can use the Parking section to manage visitor parking."
            )

        elif any(word in question for word in ["visitor", "guest", "friend", "relative"]):

            visitors = Visitor.query.filter_by(
                employee_id=current_user.id
            ).order_by(
                Visitor.created_at.desc()
            ).all()

            if visitors:
                latest = visitors[0]

                answer = (
                    f"Your latest visitor is {latest.visitor_name}. "
                    f"Visit date: {latest.visit_date.strftime('%d-%m-%Y')}. "
                    f"Status: {latest.status}. "
                    f"Parking: {latest.parking_slot or 'Not assigned'}."
                )
            else:
                answer = "You currently have no visitor records."

        elif any(word in question for word in ["food", "menu", "order", "restaurant", "eat"]):

            count = MenuItem.query.filter_by(
                available=True
            ).count()

            answer = (
                f"There are {count} food items currently available. "
                "Open Food & Dining from the dashboard to view the menu "
                "and place an order."
            )

        elif any(word in question for word in ["table", "reservation", "reserve", "dining"]):

            available_tables = 0

            from models.table import DiningTable

            available_tables = DiningTable.query.filter_by(
                status="Available"
            ).count()

            answer = (
                f"There are currently {available_tables} available dining tables. "
                "Open Table Reservation to reserve a table."
            )

        elif any(word in question for word in ["laundry", "washing", "clothes"]):

            answer = (
                "Laundry service supports washing, ironing, folding and "
                "sorting. Open Laundry from the dashboard to create a request."
            )

        elif any(word in question for word in ["facility", "maintenance", "repair", "request"]):

            answer = (
                "You can submit facility requests for maintenance or "
                "workplace services. Open Facility Requests from the dashboard."
            )

        elif any(word in question for word in ["hello", "hi", "hey"]):

            answer = (
                f"Hello {current_user.name}! 👋 "
                "I am your Smart Workspace Assistant. "
                "Ask me about parking, visitors, food, tables, laundry or facilities."
            )

        else:

            answer = (
                "I can help you with Smart Parking, Visitor Management, "
                "Food Ordering, Table Reservation, Laundry and Facility Requests."
            )

    return render_template(
        "ai_assistant.html",
        answer=answer,
        question=question
    )