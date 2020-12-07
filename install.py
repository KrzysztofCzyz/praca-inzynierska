from source.easysystems.orders.models import *
from source.easysystems.users.models import *
from source.easysystems import db, create_app, bcrypt

app = create_app()
app.app_context().push()
db.create_all()


def module_install_users():
    add_roles()
    add_users()


def module_install_orders():
    add_colors()
    add_sizes()
    add_components()
    add_ordered_components_and_product()
    add_order_items_and_orders()


def module_test_users():
    roles_test()
    users_test()


def module_test_orders():
    colors_test()
    sizes_test()
    components_test()
    ordered_components_and_product_test()
    order_items_and_orders_test()


def add_roles():
    r1 = Role(name="Admin")
    r2 = Role(name="Maszyna CNC")
    r3 = Role(name="Szycie")
    r4 = Role(name="Kontrola Jakości")
    r5 = Role(name="Pakowanie")
    r6 = Role(name="Wysyłka")

    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)
    db.session.add(r4)
    db.session.add(r5)
    db.session.add(r6)

    db.session.commit()


def add_users():
    password = bcrypt.generate_password_hash('admin123').decode('utf-8')

    u1 = User(email="admin@easysystems.pl", password=password, role=1)

    db.session.add(u1)
    db.session.commit()


def users_test():
    print(User.query.all())


def roles_test():
    print(Role.query.all())


def add_sizes():
    item1 = Size(name="XS", fabric_multiplier=0.9)
    item2 = Size(name="S", fabric_multiplier=1.0)
    item3 = Size(name="M", fabric_multiplier=1.1)
    item4 = Size(name="L", fabric_multiplier=1.2)
    item5 = Size(name="XL", fabric_multiplier=1.3)
    item6 = Size(name="XXL", fabric_multiplier=1.4)

    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.add(item4)
    db.session.add(item5)
    db.session.add(item6)
    db.session.commit()


def add_colors():
    color1 = Color(name="Niebieski")
    color2 = Color(name="Czerwony")
    color3 = Color(name="Zielony")
    color4 = Color(name="Czarny")

    db.session.add(color1)
    db.session.add(color2)
    db.session.add(color3)
    db.session.add(color4)
    db.session.commit()


def sizes_test():
    print(Size.query.all())


def colors_test():
    print(Color.query.all())


def add_components():
    c1 = Component(name="Guzik [szt] Typ 1", quantity=10, color=1)
    c2 = Component(name="Guzik [szt] Typ 1", quantity=10, color=2)
    c3 = Component(name="Guzik [szt] Typ 1", quantity=10, color=3)
    c4 = Component(name="Guzik [szt] Typ 1", quantity=10, color=4)

    xc1 = Component(name="Guzik [szt] Typ 2", quantity=10, color=1)
    xc2 = Component(name="Guzik [szt] Typ 2", quantity=10, color=2)
    xc3 = Component(name="Guzik [szt] Typ 2", quantity=10, color=3)
    xc4 = Component(name="Guzik [szt] Typ 2", quantity=10, color=4)

    cc1 = Component(name="Materiał [m2] Typ 1", quantity=10, color=1, fabric=True)
    cc2 = Component(name="Materiał [m2] Typ 1", quantity=10, color=2, fabric=True)
    cc3 = Component(name="Materiał [m2] Typ 1", quantity=10, color=3, fabric=True)
    cc4 = Component(name="Materiał [m2] Typ 1", quantity=10, color=4, fabric=True)

    xcc1 = Component(name="Materiał [m2] Typ 2", quantity=10, color=1, fabric=True)
    xcc2 = Component(name="Materiał [m2] Typ 2", quantity=10, color=2, fabric=True)
    xcc3 = Component(name="Materiał [m2] Typ 2", quantity=10, color=3, fabric=True)
    xcc4 = Component(name="Materiał [m2] Typ 2", quantity=10, color=4, fabric=True)

    xccc1 = Component(name="Nić [szp] Typ 1", quantity=10, color=1, fabric=True)
    xccc2 = Component(name="Nić [szp] Typ 1", quantity=10, color=2, fabric=True)
    xccc3 = Component(name="Nić [szp] Typ 1", quantity=10, color=3, fabric=True)
    xccc4 = Component(name="Nić [szp] Typ 1", quantity=10, color=4, fabric=True)
    
    ccc1 = Component(name="Nić [szp] Typ 2", quantity=10, color=1, fabric=True)
    ccc2 = Component(name="Nić [szp] Typ 2", quantity=10, color=2, fabric=True)
    ccc3 = Component(name="Nić [szp] Typ 2", quantity=10, color=3, fabric=True)
    ccc4 = Component(name="Nić [szp] Typ 2", quantity=10, color=4, fabric=True)

    cccc1 = Component(name="Suwak [szt]", quantity=10, color=1)
    cccc2 = Component(name="Suwak [szt]", quantity=10, color=2)
    cccc3 = Component(name="Suwak [szt]", quantity=10, color=3)
    cccc4 = Component(name="Suwak [szt]", quantity=10, color=4)

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    
    db.session.add(xc1)
    db.session.add(xc2)
    db.session.add(xc3)
    db.session.add(xc4)


    db.session.add(cc1)
    db.session.add(cc2)
    db.session.add(cc3)
    db.session.add(cc4)
    
    db.session.add(xcc1)
    db.session.add(xcc2)
    db.session.add(xcc3)
    db.session.add(xcc4)

    db.session.add(ccc1)
    db.session.add(ccc2)
    db.session.add(ccc3)
    db.session.add(ccc4)
    
    db.session.add(xccc1)
    db.session.add(xccc2)
    db.session.add(xccc3)
    db.session.add(xccc4)

    db.session.add(cccc1)
    db.session.add(cccc2)
    db.session.add(cccc3)
    db.session.add(cccc4)

    db.session.commit()


def components_test():
    print(Component.query.all())


def add_ordered_components_and_product():
    product = Product(name="Bluza")
    product2 = Product(name="Sukienka")

    p1 = OrderedComponent(component=1, quantity=4, product=product)
    p2 = OrderedComponent(component=6, quantity=3, product=product)
    p3 = OrderedComponent(component=9, quantity=1, product=product)
    p4 = OrderedComponent(component=13, quantity=1, product=product)

    p5 = OrderedComponent(component=3, quantity=2, product=product2)
    p6 = OrderedComponent(component=8, quantity=4, product=product2)
    p7 = OrderedComponent(component=11, quantity=2, product=product2)
    p8 = OrderedComponent(component=15, quantity=1, product=product2)

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(product)

    db.session.add(p5)
    db.session.add(p6)
    db.session.add(p7)
    db.session.add(p8)
    db.session.add(product2)

    db.session.commit()


def ordered_components_and_product_test():
    print(OrderedComponent.query.all())
    print(Product.query.all())


def order_items_and_orders_test():
    print(OrderItem.query.all())
    print(Order.query.all())


def add_order_items_and_orders():
    order = Order(name="Testowe zamówienie")

    i1 = OrderItem(quantity=1, product=1, size=1, order=order)
    i2 = OrderItem(quantity=1, product=2, size=6, order=order)

    db.session.add(i1)
    db.session.add(i2)
    db.session.add(order)
    db.session.commit()


module_install_users()
module_test_users()
module_install_orders()
module_test_orders()
