from app import create_app, db
from app.models import Student, Lesson, DiagnosticTest
from werkzeug.security import generate_password_hash
import json

def add_all_sample_data():
    app = create_app()
    
    with app.app_context():
        print("🚀 بدء إضافة البيانات التجريبية...")
        
        # 1. التحقق من وجود الطالب التجريبي أولاً
        existing_student = Student.query.filter_by(email='student@focus.com').first()
        if not existing_student:
            student = Student(
                username='طالب_تجريبي',
                email='student@focus.com',
                password=generate_password_hash('123456'),
                grade='1ac'
            )
            db.session.add(student)
            print("✅ تم إضافة الطالب التجريبي")
        else:
            print("⚠️  الطالب التجريبي موجود مسبقاً")
        
        # 2. إضافة الدروس التجريبية (إذا لم تكن موجودة)
        sample_lessons = [
            {
                'title': 'الرياضيات - الجبر الأساسي',
                'description': 'تعلم أساسيات الجبر والمعادلات البسيطة',
                'video_url': '/static/videos/math1.mp4',
                'subject': 'الرياضيات',
                'grade_level': '1ac',
                'duration': '15:30',
                'order': 1
            },
            {
                'title': 'الفيزياء - القوة والحركة', 
                'description': 'فهم مفاهيم القوة، السرعة، والتسارع',
                'video_url': '/static/videos/physics1.mp4',
                'subject': 'الفيزياء',
                'grade_level': '2ac',
                'duration': '20:15',
                'order': 1
            },
            {
                'title': 'اللغة العربية - النحو الأساسي',
                'description': 'تعلم الإعراب والجملة الاسمية والفعلية',
                'video_url': '/static/videos/arabic1.mp4',
                'subject': 'اللغة العربية',
                'grade_level': '1ac',
                'duration': '18:45',
                'order': 1
            }
        ]
        
        lessons_added = 0
        for lesson_data in sample_lessons:
            existing_lesson = Lesson.query.filter_by(title=lesson_data['title']).first()
            if not existing_lesson:
                lesson = Lesson(**lesson_data)
                db.session.add(lesson)
                lessons_added += 1
        
        if lessons_added > 0:
            print(f"✅ تم إضافة {lessons_added} درس تجريبي")
        else:
            print("⚠️  جميع الدروس موجودة مسبقاً")
        
        # 3. إضافة الاختبارات التجريبية (إذا لم تكن موجودة)
        sample_tests = [
            {
                'title': 'اختبار الرياضيات التشخيصي - المستوى 1',
                'subject': 'الرياضيات',
                'grade_level': '1ac',
                'description': 'اختبار تشخيصي لتقييم مستوى الطالب في الرياضيات',
                'time_limit': 30,
                'questions': [
                    {
                        'id': 1,
                        'question': 'ما هو ناتج ٥ + ٣؟',
                        'options': ['٧', '٨', '٩', '١٠'],
                        'correct_answer': 1,
                        'points': 1
                    },
                    {
                        'id': 2, 
                        'question': 'إذا كان س = ٤، فما هو ناتج س × ٣؟',
                        'options': ['٧', '١٢', '١٥', '١٦'],
                        'correct_answer': 1,
                        'points': 2
                    }
                ]
            },
            {
                'title': 'اختبار اللغة العربية التشخيصي - المستوى 1',
                'subject': 'اللغة العربية', 
                'grade_level': '1ac',
                'description': 'اختبار تشخيصي لتقييم مستوى الطالب في اللغة العربية',
                'time_limit': 25,
                'questions': [
                    {
                        'id': 1,
                        'question': 'ما هو جمع كلمة "كتاب"؟',
                        'options': ['كتب', 'كتابات', 'كتابان', 'مكاتب'],
                        'correct_answer': 0,
                        'points': 1
                    },
                    {
                        'id': 2,
                        'question': 'أي من الكلمات التالية مكتوبة بشكل صحيح؟',
                        'options': ['مدرسة', 'مدرسه', 'مدرصة', 'مدرسة'],
                        'correct_answer': 3,
                        'points': 2
                    }
                ]
            }
        ]
        
        tests_added = 0
        for test_data in sample_tests:
            existing_test = DiagnosticTest.query.filter_by(title=test_data['title']).first()
            if not existing_test:
                questions = test_data.pop('questions')
                test = DiagnosticTest(**test_data)
                test.set_questions(questions)
                db.session.add(test)
                tests_added += 1
        
        if tests_added > 0:
            print(f"✅ تم إضافة {tests_added} اختبار تشخيصي")
        else:
            print("⚠️  جميع الاختبارات موجودة مسبقاً")
        
        # حفظ كل شيء
        try:
            db.session.commit()
            print("\n🎉 تم تحديث قاعدة البيانات بنجاح!")
            
            # عرض الإحصائيات النهائية
            print("📊 الإحصائيات النهائية:")
            print(f"   - الطلاب: {Student.query.count()}")
            print(f"   - الدروس: {Lesson.query.count()}") 
            print(f"   - الاختبارات: {DiagnosticTest.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ أثناء الحفظ: {e}")

if __name__ == "__main__":
    add_all_sample_data()