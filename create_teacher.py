from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_teacher():
    app = create_app()
    
    with app.app_context():
        # التحقق من وجود المدرب
        existing_teacher = User.query.filter_by(email='teacher@focus.com').first()
        if not existing_teacher:
            teacher = User(
                username='مدرب_تجريبي',
                email='teacher@focus.com',
                password=generate_password_hash('123456'),
                role='teacher'
            )
            
            db.session.add(teacher)
            db.session.commit()
            print("✅ تم إنشاء المدرب التجريبي بنجاح!")
            print("📧 البريد: teacher@focus.com")
            print("🔑 كلمة المرور: 123456")
        else:
            print("⚠️  المدرب التجريبي موجود مسبقاً")

if __name__ == "__main__":
    create_teacher()