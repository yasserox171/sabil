from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    # تسجيل الـ blueprints
    from . import routes, auth_routes
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth_routes.auth_bp)

    return app
