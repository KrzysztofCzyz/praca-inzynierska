from flask import Blueprint, redirect, url_for, flash, render_template, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from source.easysystems import bcrypt, db
from source.easysystems.users.models import User
from source.easysystems.users.forms import LoginForm, RequestResetForm, ResetPasswordForm, RegistrationForm,\
    UpdateAccountForm
from source.easysystems.users.utils import send_reset_message, is_admin, get_roles

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    if not is_admin(current_user):
        abort(403)
    form = RegistrationForm()
    form.role.choices = get_roles()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Nowe konto zostało utworzone!', 'success')
        return redirect(url_for('users.manage_accounts'))
    return render_template('users/register.html', title='Rejestracja użytkownika', form=form)


@users.route("/accounts")
@login_required
def manage_accounts():
    if not is_admin(current_user):
        abort(403)
    user_list = User.query.except_(User.query.filter_by(id=current_user.id)).all()

    return render_template('users/managment-admin.html', title='Zarządzaj użytkownikami', user_list=user_list)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Nie udało się zalogować. Proszę sprawdzić email oraz hasło', 'danger')
    return render_template('users/login.html', title='Logowanie', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET'])
@login_required
def account():
    return render_template('users/account.html', title='Konto')


@users.route("/forgot-password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_message(user)
        flash('Wysłano e-mail z instrukcjami do zresetowania hasła', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset-request.html', title='Zapomiałem hasła', form=form)


@users.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Ten token jest niewłaściwy bądź przedawniony', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Twoje hasło zostało zaktualizowane!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset-with-token.html', title='Resetuj hasło', form=form)


@users.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Twoje hasło zostało zaktualizowane!', 'success')
        return redirect(url_for('main.home'))
    return render_template('users/change-password.html', title='Zmień hasło', form=form)


@users.route("/update-account/<int:id_>", methods=['GET', 'POST'])
@login_required
def update_account(id_):
    if not is_admin(current_user):
        abort(403)
    user = User.query.filter_by(id=id_).first_or_404()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('Konto zostało zaktualizowane!', 'success')
        return redirect(url_for('users.manage_accounts'))
    elif request.method == 'GET':
        form.email.data = user.email
    form.role.choices = get_roles()
    return render_template('users/update-account.html', title='Aktualizuj konto', form=form)


@users.route("/delete-account/<int:id_>", methods=['GET'])
@login_required
def delete_account(id_):
    if not is_admin(current_user):
        abort(403)
    user = User.query.filter_by(id=id_).first()
    if not user:
        flash('Taki użytkownik nie istnieje', 'warning')
        return redirect(url_for('users.manage_accounts'))
    if user == current_user:
        flash('Nie można usunąć swojego konta.', 'danger')
    User.query.filter_by(id=id_).delete()
    db.session.commit()
    flash('Użytkownik usunięty pomyślnie', 'success')
    return redirect(url_for('users.manage_accounts'))


