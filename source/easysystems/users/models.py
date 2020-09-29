from source.easysystems import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.role}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"