from flask_wtf import FlaskForm
from wtforms import FieldList, IntegerField, SubmitField, StringField
from wtforms.validators import ValidationError, DataRequired, Length

from source.easysystems.orders.models import Product


class GetComponentsForm(FlaskForm):
    components = FieldList(IntegerField())
    submit = SubmitField('Dodaj komponenty')


class AddProductForm(FlaskForm):
    name = StringField("Nazwa produktu", validators=[DataRequired(message='Proszę wpisać nazwę produktu'),
                                                     Length(min=5,
                                                            message='Nazwa produktu powinna mieć conajmniej 5 znaków')])
    components = FieldList(IntegerField())
    submit = SubmitField('Dodaj Produkt')

    def validate_name(self, input):
        product = Product.query.filter_by(name=input.data).first()
        if product:
            raise ValidationError('Taka nazwa produktu już istnieje')
