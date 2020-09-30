from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_required

from source.easysystems.orders.utils import get_orders_for_user

orders = Blueprint('orders', __name__)


@orders.route("/", methods=['GET', 'POST'])
@login_required
def list_orders():
    result = get_orders_for_user(current_user)
    return render_template('orders/view-orders.html', title='Zlecenia', orders=result)


@orders.route("/add", methods=['GET', 'POST'])
@login_required
def add_order():
    return render_template('orders/add-order.html', title='Dodaj zamówienie')


@orders.route("/remove/<int:id_>", methods=['GET', 'POST'])
@login_required
def remove_order(id_):
    return render_template('orders/remove-order.html', title='Usuń zamówienie')


@orders.route("/order/<int:id_>", methods=['GET', 'POST'])
@login_required
def view_order(id_):
    return render_template('orders/view-order.html', title='Usuń zamówienie')


@orders.route("/accept/<int:id_>", methods=['GET'])
@login_required
def accept_order(id_):
    pass


@orders.route("/deny/<int:id_>", methods=['GET'])
@login_required
def deny_order(id_):
    pass


@orders.route("/product/add", methods=['GET', 'POST'])
@login_required
def add_product():
    result = get_orders_for_user(current_user)
    return render_template('orders/view-orders.html', title='Zlecenia', orders=result)


@orders.route("/product/remove/<int:id_>", methods=['GET', 'POST'])
@login_required
def remove_product(id_):
    result = get_orders_for_user(current_user)
    return render_template('orders/view-orders.html', title='Zlecenia', orders=result)


# @orders.route("/product/list", methods=['GET', 'POST'])
# @login_required
# def list_products():
#     result = get_orders_for_user(current_user)
#     return render_template('orders/view-orders.html', title='Zlecenia', orders=result)
#
#
# @orders.route("/components/", methods=['GET', 'POST'])
# @login_required
# def list_products():
#     result = get_orders_for_user(current_user)
#     return render_template('orders/view-orders.html', title='Zlecenia', orders=result)
#
#
# @orders.route("/components/get", methods=['GET', 'POST'])
# @login_required
# def list_products():
#     result = get_orders_for_user(current_user)
#     return render_template('orders/view-orders.html', title='Zlecenia', orders=result)
