from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object("config.Config")
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    # مستخدم افتراضي للاختبار
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Student
        return Student.query.get(int(user_id)) if user_id else None
    
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    
    from . import routes, auth_routes
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth_routes.auth_bp)
    
    return app