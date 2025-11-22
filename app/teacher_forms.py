from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

# نموذج موحد لجميع أنواع الأسئلة
class UniversalQuestionForm(FlaskForm):
    question_type = SelectField('نوع السؤال', choices=[
        ('multiple_choice', 'متعدد الاختيارات'),
        ('true_false', 'صح/خطأ'),
        ('fill_blank', 'ملء الفراغ'),
        ('matching', 'توصيل')
    ], validators=[DataRequired()])
    
    question = StringField('السؤال', validators=[DataRequired()])
    points = IntegerField('النقاط', validators=[DataRequired(), NumberRange(min=1)], default=1)
    explanation = TextAreaField('شرح الإجابة (اختياري)')
    
    # حقول متعدد الاختيارات
    option1 = StringField('الاختيار 1')
    option2 = StringField('الاختيار 2')
    option3 = StringField('الاختيار 3')
    option4 = StringField('الاختيار 4')
    correct_choice = SelectField('الإجابة الصحيحة', choices=[
        (0, 'الاختيار 1'), (1, 'الاختيار 2'), 
        (2, 'الاختيار 3'), (3, 'الاختيار 4')
    ])
    
    # حقول صح/خطأ
    correct_bool = SelectField('الإجابة الصحيحة', choices=[
        (True, 'صح'), (False, 'خطأ')
    ])
    
    # حقول ملء الفراغ
    correct_text = StringField('الإجابة الصحيحة')
    hint_text = StringField('تلميح')
    
    # حقول التوصيل
    left_items = TextAreaField('العناصر اليسرى (سطر لكل عنصر)')
    right_items = TextAreaField('العناصر اليمنى (سطر لكل عنصر)')
    correct_matches = TextAreaField('التوصيلات الصحيحة')
    
    submit = SubmitField('إضافة السؤال')

class LessonForm(FlaskForm):
    title = StringField('عنوان الدرس', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('وصف الدرس', validators=[DataRequired()])
    subject = SelectField('المادة', choices=[
        ('الرياضيات', 'الرياضيات'),
        ('اللغة العربية', 'اللغة العربية'),
        ('الفيزياء', 'الفيزياء'),
        ('الفرنسية', 'اللغة الفرنسية')
    ], validators=[DataRequired()])
    grade_level = SelectField('المستوى', choices=[
        ('1ac', 'الإعدادي 1'),
        ('2ac', 'الإعدادي 2'),
        ('3ac', 'الإعدادي 3')
    ], validators=[DataRequired()])
    duration = StringField('مدة الدرس (دقيقة:ثانية)', validators=[DataRequired()])
    video_url = StringField('رابط الفيديو')
    document_url = StringField('رابط المستند')
    is_published = BooleanField('نشر الدرس')
    submit = SubmitField('حفظ الدرس')

class TestForm(FlaskForm):
    title = StringField('عنوان الاختبار', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('وصف الاختبار', validators=[DataRequired()])
    subject = SelectField('المادة', choices=[
        ('الرياضيات', 'الرياضيات'),
        ('اللغة العربية', 'اللغة العربية'),
        ('الفيزياء', 'الفيزياء'),
        ('الفرنسية', 'اللغة الفرنسية')
    ], validators=[DataRequired()])
    grade_level = SelectField('المستوى', choices=[
        ('1ac', 'الإعدادي 1'),
        ('2ac', 'الإعدادي 2'),
        ('3ac', 'الإعدادي 3')
    ], validators=[DataRequired()])
    time_limit = IntegerField('الوقت المحدد (دقيقة)', validators=[DataRequired(), NumberRange(min=1)])
    is_published = BooleanField('نشر الاختبار')
    submit = SubmitField('حفظ الاختبار')