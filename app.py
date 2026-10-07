from flask import Flask, render_template, redirect, url_for
from flask_login import login_required

from config import Config
from extensions import db, login_manager


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # ==========================================
    # Initialize Extensions
    # ==========================================

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # ==========================================
    # Import Models
    # ==========================================

    from models.user import User
    from models.visitor import Visitor
    from models.parking import ParkingSlot
    from models.food import MenuItem, FoodOrder, FoodOrderItem
    from models.table import DiningTable, TableReservation
    from models.laundry import LaundryRequest
    from models.facility import FacilityRequest

    # ==========================================
    # Login User Loader
    # ==========================================

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ==========================================
    # Authentication
    # ==========================================

    from routes.auth import auth
    app.register_blueprint(auth)

    # ==========================================
    # Visitor
    # ==========================================

    from routes.visitor import visitor
    app.register_blueprint(visitor)

    # ==========================================
    # Parking
    # ==========================================

    from routes.parking import parking
    app.register_blueprint(parking)

    # ==========================================
    # Food
    # ==========================================

    from routes.food import food
    app.register_blueprint(food)

    # ==========================================
    # Table Reservation
    # ==========================================

    from routes.table import table
    app.register_blueprint(table)

    # ==========================================
    # Laundry
    # ==========================================

    from routes.laundry import laundry
    app.register_blueprint(laundry)

    # ==========================================
    # Facility Requests
    # ==========================================

    from routes.facility import facility
    app.register_blueprint(facility)

    # ==========================================
    # Security Dashboard
    # ==========================================

    from routes.security import security
    app.register_blueprint(security)

    # ==========================================
    # Admin Dashboard
    # ==========================================

    from routes.admin import admin
    app.register_blueprint(admin)

     # ==========================================
    # AI Assistant
    # ==========================================
    from routes.ai_assistant import ai_assistant
    app.register_blueprint(ai_assistant)
    # ==========================================
    # ML Parking Prediction
    # ==========================================
    from routes.ml_prediction import ml_prediction
    app.register_blueprint(ml_prediction)
    # ==========================================
    # Main Dashboard
    # ==========================================

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template("dashboard.html")

    # ==========================================
    # Home → Register Page
    # ==========================================

    @app.route("/")
    def home():
        return redirect(url_for("auth.register"))

    # ==========================================
    # Create Database Tables
    # ==========================================

    with app.app_context():

        db.create_all()

        # ==========================================
        # Add Sample Food Menu
        # ==========================================

        if MenuItem.query.count() == 0:

            menu_items = [

                MenuItem(
                    name="Veg Biryani",
                    description="Aromatic vegetable biryani",
                    price=180,
                    category="Main Course",
                    available=True
                ),

                MenuItem(
                    name="Paneer Butter Masala",
                    description="Paneer cooked in creamy tomato gravy",
                    price=220,
                    category="Main Course",
                    available=True
                ),

                MenuItem(
                    name="Masala Dosa",
                    description="Crispy dosa with potato masala",
                    price=100,
                    category="South Indian",
                    available=True
                ),

                MenuItem(
                    name="Idli",
                    description="Soft steamed idli served with chutney",
                    price=60,
                    category="South Indian",
                    available=True
                ),

                MenuItem(
                    name="Veg Sandwich",
                    description="Fresh vegetable sandwich",
                    price=120,
                    category="Snacks",
                    available=True
                ),

                MenuItem(
                    name="Fresh Lime Juice",
                    description="Refreshing lime juice",
                    price=50,
                    category="Beverages",
                    available=True
                )

            ]

            db.session.add_all(menu_items)
            db.session.commit()

        # ==========================================
        # Add Sample Dining Tables
        # ==========================================

        if DiningTable.query.count() == 0:

            dining_tables = [

                DiningTable(
                    table_number="T1",
                    capacity=2,
                    status="Available"
                ),

                DiningTable(
                    table_number="T2",
                    capacity=4,
                    status="Available"
                ),

                DiningTable(
                    table_number="T3",
                    capacity=4,
                    status="Available"
                ),

                DiningTable(
                    table_number="T4",
                    capacity=6,
                    status="Available"
                ),

                DiningTable(
                    table_number="T5",
                    capacity=8,
                    status="Available"
                ),

                DiningTable(
                    table_number="T6",
                    capacity=4,
                    status="Available"
                )

            ]

            db.session.add_all(dining_tables)
            db.session.commit()

        # ==========================================
        # Add Sample Parking Slots
        # ==========================================

        if ParkingSlot.query.count() == 0:

            parking_slots = [

                ParkingSlot(
                    slot_number="B1-01",
                    floor="B1",
                    status="Available"
                ),

                ParkingSlot(
                    slot_number="B1-02",
                    floor="B1",
                    status="Available"
                ),

                ParkingSlot(
                    slot_number="B1-03",
                    floor="B1",
                    status="Available"
                ),

                ParkingSlot(
                    slot_number="B2-01",
                    floor="B2",
                    status="Available"
                ),

                ParkingSlot(
                    slot_number="B2-02",
                    floor="B2",
                    status="Available"
                ),

                ParkingSlot(
                    slot_number="B2-03",
                    floor="B2",
                    status="Available"
                ),

                ParkingSlot(
                    slot_number="B3-01",
                    floor="B3",
                    status="Available"
                ),

                ParkingSlot(
                    slot_number="B3-02",
                    floor="B3",
                    status="Available"
                )

            ]

            db.session.add_all(parking_slots)
            db.session.commit()

    # ==========================================
    # Return Application
    # ==========================================

    return app


# ==========================================
# Create Application
# ==========================================

app = create_app()


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)