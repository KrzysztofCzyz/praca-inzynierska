from source.easysystems import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    items = db.relationship('Item', backref='order', lazy=True)

    def __repr__(self):
        return f"Order('{self.name}', '{self.id}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.ForeignKey('size.id'), nullable=False)
    color = db.Column(db.ForeignKey('color.id'), nullable=False)
    parent = db.Column(db.ForeignKey('order.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', '{self.quantity}', '{self.size}', '{self.color}')"


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Color('{self.name}', '{self.id}')"


class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Size('{self.name}', '{self.id}')"
