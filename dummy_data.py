from source.easysystems.orders.models import *
from source.easysystems.users.models import *
from source.easysystems import db, create_app, bcrypt

app = create_app()
app.app_context().push()
db.create_all()

# testowanie modelu Order

order1 = Order(name="Szycie sukienek")
order2 = Order(name="Szycie sukienek 2")

db.session.add(order1)
db.session.add(order2)
db.session.commit()


test1 = Order.query.all()
test2 = test1[0].name
test3 = test1[1].id

print(test1)
print(test2)
print(test3)

# testowanie modelu Color

color1 = Color(name="Niebieski")
color2 = Color(name="Czerwony")
color3 = Color(name="Zielony")
color4 = Color(name="Czarny")

db.session.add(color1)
db.session.add(color2)
db.session.add(color3)
db.session.add(color4)
db.session.commit()

test1 = Color.query.all()
test2 = test1[0].name
test3 = test1[1].id

print(test1)
print(test2)
print(test3)

# testowanie modelu Size

item1 = Size(name="XS")
item2 = Size(name="S")
item3 = Size(name="M")
item4 = Size(name="L")
item5 = Size(name="XL")
item6 = Size(name="XXL")

db.session.add(item1)
db.session.add(item2)
db.session.add(item3)
db.session.add(item4)
db.session.add(item5)
db.session.add(item6)
db.session.commit()

test1 = Size.query.all()
test2 = test1[2].name
test3 = test1[3].id

print(test1)
print(test2)
print(test3)

# testowanie modelu Item

xitem1 = Item(name="Sukienka", quantity=100, size=1, color=2, parent=1)
xitem2 = Item(name="Sukienka", quantity=20, size=2, color=3, parent=1)
xitem3 = Item(name="Sukienka", quantity=200, size=3, color=1, parent=1)
xitem4 = Item(name="Sukienka", quantity=3, size=4, color=4, parent=2)
xitem5 = Item(name="Sukienka", quantity=34, size=3, color=3, parent=1)
xitem6 = Item(name="Sukienka", quantity=24, size=2, color=1, parent=2)

db.session.add(xitem1)
db.session.add(xitem2)
db.session.add(xitem3)
db.session.add(xitem4)
db.session.add(xitem5)
db.session.add(xitem6)
db.session.commit()

test1 = Item.query.all()
test2 = test1[2].name
test3 = test1[3].id
test4 = test1[4].parent

print(test1)
print(test2)
print(test3)
print(test4)

# testowanie modelu Role

r1 = Role(name="User")
r2 = Role(name="Admin")

db.session.add(r1)
db.session.add(r2)
db.session.commit()

test = Role.query.all()
print(test)

# testowanie modelu User

password = bcrypt.generate_password_hash('admin123').decode('utf-8')

u1 = User(email="janusz@blabla.pl", password=password, role=1)
u2 = User(email="jxxfag@fag.com", password=password, role=2)

db.session.add(u1)
db.session.add(u2)
db.session.commit()

test = User.query.all()
print(test)
print(order1.items)
