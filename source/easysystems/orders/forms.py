from flask_wtf import FlaskForm
from wtforms import FieldList, IntegerField, SubmitField


class GetComponentsForm(FlaskForm):
    components = FieldList(IntegerField(default=0))
    submit = SubmitField('Dodaj komponenty')

