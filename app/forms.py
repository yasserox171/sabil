from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired()])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6)])
    grade = SelectField('الصف الدراسي', choices=[
        ('1ep', 'الإبتدائي 1'),
        ('2ep', 'الإبتدائي 2'), 
        ('3ep', 'الإبتدائي 3'),
        ('4ep', 'الإبتدائي 4'),
        ('5ep', 'الإبتدائي 5'),
        ('6ep', 'الإبتدائي 6'),
        ('1ac', 'الإعدادي 1'),
        ('2ac', 'الإعدادي 2'),
        ('3ac', 'الإعدادي 3'),
        ('TC', 'الثانوي 1'),
        ('1bac', 'الثانوي 2'),
        ('2bac', 'الثانوي 3')
    ], validators=[DataRequired()])
    submit = SubmitField('إنشاء حساب')

class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    submit = SubmitField('تسجيل الدخول')