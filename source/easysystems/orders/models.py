from source.easysystems import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    position = db.Column(db.ForeignKey('role.id'), nullable=False, default=1)  # zakłada role admina
    message = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"Order('{self.name}', '{self.id}')"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.Column(db.ForeignKey('product.id'), nullable=False)
    size = db.Column(db.ForeignKey('size.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('items', lazy=True), lazy=True)
    order_fk = db.Column(db.ForeignKey('order.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.quantity}', '{self.size}')"


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Color('{self.name}', '{self.id}')"


class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    fabric_multiplier = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Size('{self.name}', '{self.id}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Product('{self.name}')"


class OrderedComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    component = db.Column(db.ForeignKey('component.id'), nullable=False)
    product_fk = db.Column(db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('components', lazy=True), lazy=True)

    def __repr__(self):
        return f"OrderedComponent('{self.quantity}', '{self.component}')"


class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    color = db.Column(db.ForeignKey('color.id'), nullable=False)
    fabric = db.Column(db.Boolean, nullable=False, default=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Component('{self.name}', '{self.quantity}')"
