from app import create_app, db
from app.models import Lesson

app = create_app()

with app.app_context():
    # بيانات الدروس التجريبية
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
        },
        {
            'title': 'الرياضيات - الهندسة المستوية',
            'description': 'دراسة الأشكال الهندسية الأساسية ونظرياتها',
            'video_url': '/static/videos/math2.mp4',
            'subject': 'الرياضيات',
            'grade_level': '2ac',
            'duration': '22:10',
            'order': 2
        },
        {
            'title': 'الفرنسية - القواعد الأساسية',
            'description': 'تعلم قواعد اللغة الفرنسية للمبتدئين',
            'video_url': '/static/videos/french1.mp4',
            'subject': 'اللغة الفرنسية',
            'grade_level': '1ac',
            'duration': '16:20',
            'order': 1
        }
    ]
    
    # إضافة الدروس إلى قاعدة البيانات
    for lesson_data in sample_lessons:
        lesson = Lesson(**lesson_data)
        db.session.add(lesson)
    
    db.session.commit()
    print("✅ تم إضافة الدروس التجريبية بنجاح!")