from app import create_app, db
from app.models import User, Lesson, DiagnosticTest
from werkzeug.security import generate_password_hash

def update_database():
    app = create_app()
    
    with app.app_context():
        print("🔄 تحديث قاعدة البيانات...")
        
        # حذف الجداول القديمة وإعادة إنشائها
        db.drop_all()
        db.create_all()
        print("✅ تم إنشاء الجداول الجديدة")
        
        # إنشاء مدرب تجريبي
        teacher = User(
            username='مدرب_تجريبي',
            email='teacher@focus.com',
            password=generate_password_hash('123456'),
            role='teacher'
        )
        db.session.add(teacher)
        print("✅ تم إنشاء المدرب التجريبي")
        
        # إنشاء طالب تجريبي
        student = User(
            username='طالب_تجريبي',
            email='student@focus.com',
            password=generate_password_hash('123456'),
            role='student',
            grade='1ac'
        )
        db.session.add(student)
        print("✅ تم إنشاء الطالب التجريبي")
        
        # إضافة بعض الدروس التجريبية
        sample_lessons = [
            {
                'title': 'الرياضيات - الجبر الأساسي',
                'description': 'تعلم أساسيات الجبر والمعادلات البسيطة',
                'video_url': '/static/videos/math1.mp4',
                'subject': 'الرياضيات',
                'grade_level': '1ac',
                'duration': '15:30',
                'order': 1,
                'is_published': True,
                'created_by': 1  # المدرب الأول
            },
            {
                'title': 'الفيزياء - القوة والحركة',
                'description': 'فهم مفاهيم القوة، السرعة، والتسارع',
                'video_url': '/static/videos/physics1.mp4',
                'subject': 'الفيزياء',
                'grade_level': '2ac',
                'duration': '20:15',
                'order': 1,
                'is_published': True,
                'created_by': 1
            }
        ]
        
        for lesson_data in sample_lessons:
            lesson = Lesson(**lesson_data)
            db.session.add(lesson)
        print("✅ تم إضافة الدروس التجريبية")
        
        # إضافة اختبار تجريبي
        test = DiagnosticTest(
            title='اختبار الرياضيات التشخيصي - المستوى 1',
            subject='الرياضيات',
            grade_level='1ac',
            description='اختبار تشخيصي لتقييم مستوى الطالب في الرياضيات',
            time_limit=30,
            is_published=True,
            created_by=1,
            questions='[]'
        )
        db.session.add(test)
        print("✅ تم إضافة الاختبار التجريبي")
        
        # حفظ كل شيء
        db.session.commit()
        
        print("\n🎉 تم تحديث قاعدة البيانات بنجاح!")
        print("📊 الإحصائيات النهائية:")
        print(f"   👨‍🏫 المدربين: {User.query.filter_by(role='teacher').count()}")
        print(f"   👨‍🎓 الطلاب: {User.query.filter_by(role='student').count()}")
        print(f"   📚 الدروس: {Lesson.query.count()}")
        print(f"   🎯 الاختبارات: {DiagnosticTest.query.count()}")
        
        print("\n🔑 بيانات الدخول:")
        print("   👨‍🏫 المدرب: teacher@focus.com / 123456")
        print("   👨‍🎓 الطالب: student@focus.com / 123456")

if __name__ == "__main__":
    update_database()