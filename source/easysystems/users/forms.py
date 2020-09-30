from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from source.easysystems.users.models import User


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class RequestResetForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    submit = SubmitField('Resetuj hasło')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('Nie ma takiego adresu e-mail w bazie.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Hasło', validators=[DataRequired(),
                                                  Length(6, 20, 'Hasło powinno mieć pomiędzy 6 a 20 znaków')])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zmień hasło')


class RegistrationForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired(),
                                                  Length(6, 20, 'Hasło powinno mieć pomiędzy 6 a 20 znaków')])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Funkcja',  validators=[DataRequired()], validate_choice=True)
    submit = SubmitField('Zapisz użytkowinka')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Istnieje już taki adres e-mail w bazie. Proszę wybrać inny')


class UpdateAccountForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    role = SelectField('Funkcja', validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Aktualizuj')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        user_id = repr(request.base_url).split('/')[-1][:-1]
        user_email = User.query.filter_by(id=user_id).first()
        if email and email != user_email:
            raise ValidationError('Istnieje już taki adres e-mail w bazie. Proszę wybrać inny')
