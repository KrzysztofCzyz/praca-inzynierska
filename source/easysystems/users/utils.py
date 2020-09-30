from mailbox import Message
from source.easysystems.users.models import Role
from source.easysystems import mail

from flask import url_for, abort


def is_admin(user):
    return role_from_id(user.id) == 'Admin'


def role_from_id(id_):
    role = Role.query.filter_by(id=id_).first()
    if role:
        return role.name
    else:
        abort(500)


def get_roles():
    roles = Role.query.all()
    result = []

    def map_fun(item):
        result.append((item.id, item.name))

    return map(map_fun, roles)


def send_reset_message(user):
    token = user.get_reset_token()
    message = Message('Żądanie resetu hasła',
                  sender='noreply@easysystems.pl',
                  recipients=[user.email], )
    message.body = f'''Aby zmienić hasło, kliknij poniższy link:
{url_for('users.reset_token', token=token, _external=True)}

Jeżeli ten mail nie był zainicjowany przez Ciebie, prosimy zignorować tę wiadomość.

Pozdrawiamy,
EasySystems Team'''
    mail.send(message)
