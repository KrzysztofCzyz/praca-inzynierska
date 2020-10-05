from flask import abort

from source.easysystems.orders.models import *
from source.easysystems import db
from source.easysystems.users.utils import role_from_id


def get_product_by_id(id_):
    result = Product.query.filter_by(id=id_).first()
    if result:
        return result
    else:
        abort(500)


def get_size_by_id(id_):
    result = Size.query.filter_by(id=id_).first()
    if result:
        return result
    else:
        abort(500)


def get_sizes():
    result = Size.query.all()
    return result


def get_products():
    result = Product.query.all()
    return result


def get_orders_for_user(user):
    order_list = Order.query.except_(Order.query.filter_by(completed=True)).filter_by(position=user.role).all()
    return order_list


def get_components():
    components = Component.query.all()
    return components


def color_from_id(id_):
    result = Color.query.filter_by(id=id_).first()
    if result:
        return result.name
    else:
        abort(500)


def get_component_by_id(id_):
    result = Component.query.filter_by(id=id_).first()
    if result:
        return result
    else:
        abort(500)


def advance_order(order):
    if role_from_id(order.position) == 'Pakowanie':
        order.completed = True
        db.session.commit()
        return
    order.position += 1
    db.session.commit()


def deny_order(order, message):
    if role_from_id(order.position) == 'Kontrola Jakości':
        order.position -= 1
    order.message = message
    db.session.commit()
