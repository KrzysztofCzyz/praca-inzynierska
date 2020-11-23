from flask import abort

from source.easysystems.orders.models import *
from source.easysystems import db
from source.easysystems.users.utils import role_from_id, is_admin

import json


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
    order_list = Order.query.except_(Order.query.filter_by(completed=True))
    if not is_admin(user):
        return order_list.filter_by(position=user.role).filter_by(requires_action=False).all()
    else:
        return order_list.all()


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
    else:
        order.requires_action = True
    order.message = message
    db.session.commit()


def get_raport(data):
    component_report = {"components": []}
    for c in data:
        component_report["components"].append(c.to_json())
    return component_report


def calculate_data_for_order(order):
    final_list = []
    order_list = []
    for i in order.items:
        item_q = i.quantity
        f_multiplier = get_size_by_id(i.size).fabric_multiplier
        pr = get_product_by_id(i.product)
        o_components = pr.components
        components = list(map(lambda component: (get_component_by_id(component.component).id,
                                                 get_component_by_id(component.component).fabric,
                                                 component.quantity), o_components))
        result = list(map(lambda x: x[1] and (x[0], x[2] * item_q * f_multiplier) or (x[0], x[2] * item_q), components))
        order_list.extend(result)
    temp_dic = {}
    for item in order_list:
        if item[0] in temp_dic.keys():
            temp_dic[item[0]] += item[1]
        else:
            temp_dic[item[0]] = item[1]

    for k in temp_dic.keys():
        final_list.append((k, temp_dic.get(k)))

    return list(map(lambda x: (get_component_by_id(x[0]),
                               round(get_component_by_id(x[0]).quantity - x[1], 1)), final_list))
