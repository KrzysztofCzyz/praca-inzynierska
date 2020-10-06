from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_mail import Mail
from source.easysystems.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = 'info'
login_manager.login_message = "Zaloguj się aby uzyskać dostęp do tej strony."
# mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # mail.init_app(app)

    from source.easysystems.errors.handlers import errors
    from source.easysystems.main.routes import main
    from source.easysystems.users.routes import users
    from source.easysystems.orders.routes import orders
    from source.easysystems.users.utils import role_from_id, is_admin
    from source.easysystems.orders.utils import color_from_id, get_component_by_id, get_product_by_id, get_size_by_id

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(orders, url_prefix='/orders')

    app.jinja_env.globals.update(role_from_id=role_from_id)
    app.jinja_env.globals.update(is_admin=is_admin)
    app.jinja_env.globals.update(color_from_id=color_from_id)
    app.jinja_env.globals.update(get_component_by_id=get_component_by_id)
    app.jinja_env.globals.update(get_product_by_id=get_product_by_id)
    app.jinja_env.globals.update(get_size_by_id=get_size_by_id)

    return app
