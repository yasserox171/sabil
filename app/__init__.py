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
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # ✅ تأكد من أن هذا هو User وليس Student
        return User.query.get(int(user_id)) if user_id else None
    
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    
    # ✅ تسجيل الـ Blueprints
    from . import routes
    from . import teacher_routes
    
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(teacher_routes.teacher_bp)
    
    return app