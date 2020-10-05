from flask_wtf import FlaskForm
from wtforms import FieldList, IntegerField, SubmitField, StringField, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length

from source.easysystems.orders.models import Product, Size


class GetComponentsForm(FlaskForm):
    components = FieldList(IntegerField())
    submit = SubmitField('Dodaj komponenty')


class AddProductForm(FlaskForm):
    name = StringField('Nazwa produktu', validators=[DataRequired(message='Proszę wpisać nazwę produktu'),
                                                     Length(min=5,
                                                            message='Nazwa produktu powinna mieć conajmniej 5 znaków')])
    components = FieldList(IntegerField())
    submit = SubmitField('Dodaj Produkt')

    def validate_name(self, input):
        product = Product.query.filter_by(name=input.data).first()
        if product:
            raise ValidationError('Taka nazwa produktu już istnieje')


class AddOrderForm(FlaskForm):
    name = StringField('Nazwa zamówienia',
                       validators=[DataRequired(message='Proszę wpisać nazwę zamówienia'),
                                   Length(min=5, message='Nazwa zamówienia powinna mieć conajmniej 5 znaków')])
    submit = SubmitField('Dodaj zamówienie')


class AddOrderItemForm(FlaskForm):
    product = SelectField('Produkt', validators=[DataRequired()], validate_choice=False)
    quantity = IntegerField('Ilość produktu')
    size = SelectField('Rozmiar', validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Dodaj produkt do zamówienia')

    def validate_quantity(self, quantity):
        if quantity.data < 0:
            raise ValidationError('Ilość produktu nie może być mniejsza od zera')


class MessageForm(FlaskForm):
    message = StringField('Wiadomość', validators=[DataRequired()])
    accept = BooleanField('Akceptuj?')
    submit = SubmitField('Gotowe')
