from source.easysystems.users.models import Role

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