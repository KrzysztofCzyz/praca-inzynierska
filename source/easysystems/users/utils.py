from mailbox import Message
from source.easysystems.users.models import Role
from source.easysystems import mail

from flask import url_for, abort


def is_admin(user):
    return role_from_id(user.role) == 'Admin'


def role_from_id(id_):
    role = Role.query.filter_by(id=id_).first()
    if role is not None:
        return role.name
    else:
        abort(500)


def get_roles():
    roles = Role.query.all()

    def map_fun(item):
        return item.id, item.name

    result = list(map(map_fun, roles))
    return result


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
