from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_required
from math import floor

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
    if not is_admin(current_user):
        abort(404)
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
    remove_item_from_order(item)
    flash('Pomyślnie usunięto przedmiot z zamówienia', 'success')
    return redirect(url_for('orders.launch_order', id_=order.id))


@orders.route("/order/edit/<int:id_>", methods=['GET', 'POST'])
@login_required
def edit_order(id_):
    if not is_admin(current_user):
        abort(403)
    order = Order.query.filter_by(id=id_).first_or_404()
    if order.position != 1:
        abort(404)
    form = IntegralForm()
    labels = []
    for e in order.items:
        labels.append(f"{e.id}: {get_product_by_id(e.product).name}, rozmiar {get_size_by_id(e.size).name}")
    if form.validate_on_submit():
        i = 0
        for field in form.components.entries:
            item_id = int(labels[i].split(":")[0])
            i += 1
            item = OrderItem.query.filter_by(id=item_id).first_or_404()
            if field.data < 1:
                remove_item_from_order(item)
            else:
                item.quantity = field.data
        db.session.commit()
        flash('Dane zmieniono pomyślnie', 'success')
        return redirect(url_for('orders.launch_order', id_=order.id))
    elif request.method == 'GET':
        for e in order.items:
            form.components.append_entry(data=e.quantity)
    return render_template('orders/edit-order.html', title='Edytuj pozycje zamówienia', form=form, items=order.items, labels=labels)


@orders.route("/order/split/<int:id_>", methods=['GET', 'POST'])
@login_required
def split_order(id_):
    if not is_admin(current_user):
        abort(403)
    order = Order.query.filter_by(id=id_).first_or_404()
    if order.position != 1:
        abort(404)
    form = IntegralForm()
    labels = []
    for e in order.items:
        labels.append(f"{e.id}: {get_product_by_id(e.product).name}, rozmiar {get_size_by_id(e.size).name}, obecna ilość {e.quantity}")
    if form.validate_on_submit():
        i = 0
        order2 = Order(name=order.name+' - część 2')
        new_items = False
        for field in form.components.entries:
            item_id = int(labels[i].split(":")[0])
            i += 1
            item = OrderItem.query.filter_by(id=item_id).first_or_404()
            if field.data < 1:
                new_item = OrderItem(quantity=item.quantity, product=item.product, order=order2, size=item.size)
                db.session.delete(item)
                db.session.add(new_item)
                new_items = True
            elif field.data < item.quantity:
                diff = item.quantity - field.data
                new_item = OrderItem(quantity=diff, product=item.product, order=order2, size=item.size)
                item.quantity -= field.data
                db.session.add(new_item)
                new_items = True
        if new_items:
            db.session.add(order2)
            db.session.commit()
            flash('Pomyślnie rozdzielono zamówienia', 'success')
        else:
            flash('Brak produktów do rodzielenia', 'info')
        return redirect(url_for('orders.list_orders'))
    elif request.method == 'GET':
        for e in order.items:
            form.components.append_entry(data=e.quantity)
    return render_template('orders/split-order.html', title='Podziel zamówienie', form=form, items=order.items, labels=labels)


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
            add_item_to_order(form.quantity.data, form.product.data, id_, form.size.data)
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
    return redirect(url_for('orders.list_orders'))


@orders.route("/order/poke/<int:id_>", methods=['GET'])
@login_required
def perform_action(id_):
    if not is_admin(current_user):
        abort(403)
    order = Order.query.filter_by(id=id_).first_or_404()
    if order.requires_action is True:
        order.message = ""
        order.requires_action = False
        db.session.commit()
    return redirect(url_for('orders.list_orders'))


@orders.route("/order/<int:id_>", methods=['GET', 'POST'])
@login_required
def view_order(id_):
    order = Order.query.filter_by(id=id_).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        if form.accept.data:
            advance_order(order)
            flash('Zamówienie ' + order.name + ' zostało zaakceptowane!', 'success')
        else:
            deny_order(order, form.message.data)
            flash('Zamówienie ' + order.name + ' zostało odrzucone!', 'info')
        return redirect(url_for('orders.list_orders'))
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
    final_list = calculate_data_for_order(order)
    missing_data = []
    for i in final_list:
        if i[1] < 0:
            missing_data.append({"nazwa": i[0].name, "kolor": i[0].color, "ilosc": i[1]})

    if form.validate_on_submit():
        for i in final_list:
            i[0].quantity = i[1]
        order.position += 1
        db.session.commit()
        flash('Pomyślnie uruchomiono zamówienie ' + order.name, 'success')
        return redirect(url_for('orders.view_order', id_=order.id))

    return render_template('orders/launch-order.html', title='Uruchom zamówienie', order=order, form=form,
                           item_list=final_list, missing_data=missing_data)


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
    o = OrderItem.query.filter_by(product=result.id).first()
    if o:
        flash('Produkt znajduje się w użyciu. Nie można go usunąć!', 'info')
        return redirect(url_for('orders.list_products'))
    for component in result.components:
        db.session.delete(component)
    db.session.delete(result)
    db.session.commit()
    flash('Pomyślnie usunięto produkt: ' + result.name, 'success')
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
                    if r.fabric:
                        r.quantity += field.data
                    else:
                        r.quantity += floor(field.data)
        db.session.commit()
        flash('Komponenty dodane pomyślnie', 'success')
        return redirect(url_for('orders.list_components'))
    elif request.method == 'GET':
        for e in result:
            form.components.append_entry(data=0)
    return render_template('orders/get-components.html', title='Uzupełnij komponenty', form=form, labels=labels)


@orders.route("/components/report", methods=['GET'])
@login_required
def report_components():
    if not is_admin(current_user):
        abort(403)
    components = Component.query.all()
    report = get_raport(components)
    return render_template('orders/report.html', title='Komponenty w bazie - Raport', report=report["components"])


@orders.route("/components/report/<int:id_>", methods=['GET', 'POST'])
@login_required
def report_missing_components(id_):
    if not is_admin(current_user):
        abort(403)
    order = Order.query.filter_by(id=id_).first_or_404()
    form = GetComponentsForm()
    result = get_components()
    r2 = calculate_data_for_order(order)
    ids = list(map(lambda x: x[0].id, r2))
    labels = []
    for e in result:
        labels.append(f"{e.id}: {color_from_id(e.color)} {e.name}, Stan po operacji: {list(filter(lambda x: x[0].id == e.id, r2))[0][1] if e.id in ids else e.quantity} Zamów:")
    if form.validate_on_submit():
        missing_data = []
        result = get_components()
        for field in form.components.entries:
            item_id = int(field.label.text.split('-')[1]) + 1
            for r in result:
                if r.id == item_id and field.data > 0:
                    missing_data.append({"nazwa": r.name, "kolor": r.color, "ilosc": field.data})
        report = {"components": missing_data}
        flash('Raport utworzony pomyślnie', 'success')
        return render_template('orders/report.html', title=order.name + ' - Raport', report=report)
    elif request.method == 'GET':
        for e in result:
            val = list(filter(lambda x: x[0].id == e.id and x[1] < 0, r2) if e.id in ids else [(0, 0)])
            form.components.append_entry(data=abs(val[0][1]) if val else 0)
        form.submit.label.text = "Generuj"
    return render_template('orders/get-components.html', title=order.name+" - Raport", form=form, labels=labels)
