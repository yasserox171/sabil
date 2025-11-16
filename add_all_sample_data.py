from app import create_app, db
from app.models import Student, Lesson, DiagnosticTest
from werkzeug.security import generate_password_hash
import json

def add_all_sample_data():
    app = create_app()
    
    with app.app_context():
        print("🚀 بدء إضافة البيانات التجريبية...")
        
        # 1. إضافة طالب تجريبي
        student = Student(
            username='طالب_تجريبي',
            email='student@focus.com',
            password=generate_password_hash('123456'),
            grade='1ac'
        )
        db.session.add(student)
        print("✅ تم إضافة الطالب التجريبي")
        
        # 2. إضافة الدروس التجريبية
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
        
        for lesson_data in sample_lessons:
            lesson = Lesson(**lesson_data)
            db.session.add(lesson)
        print("✅ تم إضافة الدروس التجريبية")
        
        # 3. إضافة الاختبارات التجريبية
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
        
        for test_data in sample_tests:
            questions = test_data.pop('questions')
            test = DiagnosticTest(**test_data)
            test.set_questions(questions)
            db.session.add(test)
        print("✅ تم إضافة الاختبارات التشخيصية")
        
        # حفظ كل شيء
        db.session.commit()
        
        print("\n🎉 تم إضافة جميع البيانات التجريبية بنجاح!")
        print("📊 الإحصائيات:")
        print(f"   - الطلاب: {Student.query.count()}")
        print(f"   - الدروس: {Lesson.query.count()}") 
        print(f"   - الاختبارات: {DiagnosticTest.query.count()}")

if __name__ == "__main__":
    add_all_sample_data()