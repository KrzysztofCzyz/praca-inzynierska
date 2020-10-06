import itertools

from flask import Blueprint, redirect, url_for, flash, render_template, request, abort
from flask_login import current_user, login_required


from source.easysystems.users.utils import is_admin
from source.easysystems.orders.utils import *
from source.easysystems.orders.forms import *

orders = Blueprint('orders', __name__)


@orders.route("/", methods=['GET', 'POST'])
@login_required
def list_orders():
    result = get_orders_for_user(current_user)
    return render_template('orders/view-orders.html', title='Zamówienia', orders=result)


@orders.route("/order/add", methods=['GET', 'POST'])
@login_required
def add_order():
    form = AddOrderForm()
    if form.validate_on_submit():
        order = Order(name=form.name.data)
        db.session.add(order)
        db.session.commit()
        flash('Pomyślnie dodano zamówienie', 'success')
        return redirect(url_for('orders.add_order_item', id_=order.id))
    return render_template('orders/add-order.html', title='Dodaj zamówienie', form=form)


@orders.route("/order/remove-item/<int:id_>", methods=['GET'])
@login_required
def remove_order_item(id_):
    if not is_admin(current_user):
        abort(403)
    item = OrderItem.query.filter_by(id=id_).first_or_404()
    order = Order.query.filter_by(id=item.order_fk).first_or_404()
    if order.position != 1:
        flash('Nie można usuwać przedmiotów z uruchomionych zamównień', 'danger')
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Pomyślnie usunięto przedmiot z zamówienia', 'success')
    return redirect(url_for('orders.launch_order', id_=order.id))


@orders.route("/order/add-item/<int:id_>", methods=['GET', 'POST'])
@login_required
def add_order_item(id_):
    if not is_admin(current_user):
        abort(403)
    order = Order.query.filter_by(id=id_).first_or_404()
    if order.position != 1:
        abort(404)
    if order.items:
        order_products = list(map(lambda item: item.product, order.items))
    else:
        order_products = list()
    form = AddOrderItemForm()
    products = get_products()
    result = list(map(lambda product: (product.id, product.name), products))
    form.product.choices = result
    sizes = get_sizes()
    result = list(map(lambda size: (size.id, size.name), sizes))
    form.size.choices = result
    if form.validate_on_submit():
        if form.product.data in order_products:
            flash('Ten produkt istnieje już w Twoim zamówieniu!', 'danger')
        else:
            print(form.quantity.data, form.product.data, form.size.data, id_, form.size.data)
            order_item = OrderItem(quantity=form.quantity.data, product=form.product.data,
                                   order_fk=id_, size=form.size.data)
            db.session.add(order_item)
            db.session.commit()
            flash('Pomyślnie dodano nową pozycję w zamówieniu', 'success')
            return redirect(url_for('orders.launch_order', id_=id_))
    return render_template('orders/add-order-item.html', title='Dodaj pozycję do zamówienia', form=form)


@orders.route("/order/remove/<int:id_>", methods=['GET'])
@login_required
def remove_order(id_):
    if not is_admin(current_user):
        abort(403)
    order = Order.query.filter_by(id=id_).first_or_404()
    if order.position != 1:
        abort(404)
    for item in order.items:
        db.session.delete(item)
    db.session.delete(order)
    db.session.commit()
    flash('Pomyślnie usunięto to zamówienie', 'success')
    return render_template('orders/remove-order.html', title='Usuń zamówienie')


@orders.route("/order/<int:id_>", methods=['GET'])
@login_required
def view_order(id_):
    order = Order.query.filter_by(id=id_).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        if form.accept.checked:
            advance_order(order)
        else:
            deny_order(order, form.message.data)
    return render_template('orders/view-order.html', title='Szczegóły zamówienia', order=order, form=form)


@orders.route("/order/launch/<int:id_>", methods=['GET', 'POST'])
@login_required
def launch_order(id_):
    if not is_admin(current_user):
        abort(403)
    order = Order.query.filter_by(id=id_).first_or_404()
    if order.position != 1:
        flash('Zamówienie jest już uruchomione', 'info')
        redirect(url_for('orders.view_order', id_=id_))
    form = LaunchForm()
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
        result = list(map(lambda x: x[1] and (x[0], x[2]*item_q*f_multiplier) or (x[0], x[2]*item_q), components))
        order_list.extend(result)
    for k, g in itertools.groupby(order_list, key=lambda x: x[0]):
        final_list.append((k, sum(list(map(lambda x: x[1], g)))))
    final_list = map(lambda x: (get_component_by_id(x[0]), round(get_component_by_id(x[0]).quantity-x[1], 1)),
                     final_list)
    if form.validate_on_submit():
        for i in final_list:
            i[0].quantity = i[1]
        order.position += 1
        db.session.commit()
        flash('Pomyślnie uruchomiono zamówienie ' + order.name, 'success')
    return render_template('orders/launch-order.html', title='Uruchom zamówienie', order=order, form=form,
                           item_list=final_list)


@orders.route("/products/list", methods=['GET'])
@login_required
def list_products():
    result = get_products()
    return render_template('orders/view-products.html', title='Produkty', products=result)


@orders.route("/products/add", methods=['GET', 'POST'])
@login_required
def add_product():
    if not is_admin(current_user):
        abort(403)
    form = AddProductForm()
    result = get_components()
    labels = []
    for e in result:
        labels.append(f"{e.name}: {color_from_id(e.color)}")
    if form.validate_on_submit():
        product = Product(name=form.name.data)
        for field in form.components.entries:
            if field.data > 0:
                item_id = int(field.label.text.split('-')[1]) + 1
                component = OrderedComponent(quantity=field.data, component=item_id, product=product)
                db.session.add(component)
        if len(product.components) > 0:
            db.session.add(product)
            db.session.commit()
            flash('Produkt dodany pomyślnie', 'success')
            return redirect(url_for('orders.list_products'))
        else:
            flash('Nie dodano żadnego komponentu. Produkt nie zostanie dodany', 'danger')
    elif request.method == 'GET':
        for e in result:
            form.components.append_entry(data=0)
    return render_template('orders/add-product.html', title='Dodaj produkt', form=form, labels=labels)


@orders.route("/products/remove/<int:id_>", methods=['GET'])
@login_required
def remove_product(id_):
    if not is_admin(current_user):
        abort(403)
    result = Product.query.filter_by(id=id_).first_or_404()
    for component in result.components:
        db.session.delete(component)
    db.session.delete(result)
    db.session.commit()
    flash('Pomyślnie usunięto produkt ' + result.name, 'success')
    return redirect(url_for('orders.list_products'))


@orders.route("/components/list", methods=['GET'])
@login_required
def list_components():
    result = get_components()
    return render_template('orders/view-components.html', title='Komponenty', components=result)


@orders.route("/components/get", methods=['GET', 'POST'])
@login_required
def add_components():
    if not is_admin(current_user):
        abort(403)
    form = GetComponentsForm()
    result = get_components()
    labels = []
    for e in result:
        labels.append(f"{e.id}: {color_from_id(e.color)} {e.name}, Stan: {e.quantity}")
    if form.validate_on_submit():
        result = get_components()
        for field in form.components.entries:
            item_id = int(field.label.text.split('-')[1])+1
            for r in result:
                if r.id == item_id:
                    r.quantity += field.data
        db.session.commit()
        flash('Komponenty dodane pomyślnie', 'success')
        return redirect(url_for('orders.list_components'))
    elif request.method == 'GET':
        for e in result:
            form.components.append_entry(data=0)
    return render_template('orders/get-components.html', title='Dodaj komponenty', form=form, labels=labels)
