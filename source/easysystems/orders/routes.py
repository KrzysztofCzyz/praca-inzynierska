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
