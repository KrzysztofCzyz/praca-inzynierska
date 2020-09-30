from source.easysystems.users.models import User
from source.easysystems.orders.models import Order

from source.easysystems import db
from source.easysystems.users.utils import role_from_id


def get_orders_for_user(user):
    order_list = Order.query.except_(Order.query.filter_by(completed=True)).filter_by(position=user.role).all()
    return order_list


def advance_order(order, message):
    if role_from_id(order.position) == 'Pakowanie':
        order.message = message
        order.completed = True
        db.session.commit()
        return
    order.position += 1
    order.message = message
    db.session.commit()


def deny_order(order, message):
    if role_from_id(order.position) == 'Kontrola Jakości':
        order.position -= 1
    order.message = message
    db.session.commit()
