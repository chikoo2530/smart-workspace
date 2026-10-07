from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.food import MenuItem, FoodOrder, FoodOrderItem


food = Blueprint("food", __name__)


# =========================================================
# FOOD MENU
# =========================================================

@food.route("/food")
@login_required
def food_menu():

    menu_items = MenuItem.query.filter_by(
        available=True
    ).all()

    return render_template(
        "food/menu.html",
        menu_items=menu_items
    )


# =========================================================
# PLACE FOOD ORDER
# =========================================================

@food.route("/food/order", methods=["POST"])
@login_required
def place_order():

    item_ids = request.form.getlist("item_id")
    quantities = request.form.getlist("quantity")

    if not item_ids:

        flash(
            "Please select at least one food item.",
            "warning"
        )

        return redirect(
            url_for("food.food_menu")
        )

    order = FoodOrder(
        user_id=current_user.id,
        total_amount=0,
        status="Payment Pending"
    )

    db.session.add(order)
    db.session.flush()

    total = 0

    for item_id, quantity in zip(
        item_ids,
        quantities
    ):

        menu_item = db.session.get(
            MenuItem,
            int(item_id)
        )

        if not menu_item:
            continue

        if not menu_item.available:
            continue

        quantity = int(quantity)

        if quantity <= 0:
            continue

        item_total = (
            menu_item.price * quantity
        )

        total += item_total

        order_item = FoodOrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=quantity,
            price=menu_item.price
        )

        db.session.add(order_item)

    # No valid items
    if total <= 0:

        db.session.rollback()

        flash(
            "Please select valid food items.",
            "warning"
        )

        return redirect(
            url_for("food.food_menu")
        )

    order.total_amount = total

    db.session.commit()

    # Go to payment page
    return redirect(
        url_for(
            "food.payment",
            order_id=order.id
        )
    )


# =========================================================
# PAYMENT PAGE
# =========================================================

@food.route("/food/payment/<int:order_id>")
@login_required
def payment(order_id):

    order = FoodOrder.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "food/payment.html",
        order=order
    )


# =========================================================
# CONFIRM PAYMENT
# =========================================================

@food.route(
    "/food/payment/<int:order_id>/confirm",
    methods=["POST"]
)
@login_required
def confirm_payment(order_id):

    order = FoodOrder.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first_or_404()

    payment_method = request.form.get(
        "payment_method"
    )

    if not payment_method:

        flash(
            "Please select a payment method.",
            "warning"
        )

        return redirect(
            url_for(
                "food.payment",
                order_id=order.id
            )
        )

    # Demo payment confirmation
    order.status = "Confirmed"

    db.session.commit()

    flash(
        f"Payment successful using {payment_method}. "
        f"Order #{order.id} confirmed.",
        "success"
    )

    return redirect(
        url_for("food.my_orders")
    )


# =========================================================
# MY ORDERS
# =========================================================

@food.route("/food/orders")
@login_required
def my_orders():

    orders = FoodOrder.query.filter_by(
        user_id=current_user.id
    ).order_by(
        FoodOrder.created_at.desc()
    ).all()

    return render_template(
        "food/orders.html",
        orders=orders
    )