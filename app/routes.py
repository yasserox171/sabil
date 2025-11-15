from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import RegisterForm, LoginForm
from .models import Lesson, Student
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # ✅ إنشاء الفورم
    
    if form.validate_on_submit():
        # هنا سيأتي كود التحقق من تسجيل الدخول
        student = Student.query.filter_by(email=form.email.data).first()
        if student and check_password_hash(student.password, form.password.data):
            flash('✅ تم تسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('❌ البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
    
    # ✅ تمرير الفورم إلى القالب
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # ✅ إنشاء الفورم
    
    if form.validate_on_submit():
        # التحقق من عدم وجود مستخدم بنفس البريد
        existing_user = Student.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('❌ هذا البريد الإلكتروني مسجل بالفعل!', 'danger')
            return redirect(url_for('main.register'))
        
        # إنشاء مستخدم جديد
        hashed_password = generate_password_hash(form.password.data)
        new_student = Student(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            grade=form.grade.data
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        flash('✅ تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.', 'success')
        return redirect(url_for('main.login'))
    
    # ✅ تمرير الفورم إلى القالب
    return render_template('register.html', form=form)

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/lessons')
def lessons():
    return render_template('lessons.html')

@main_bp.route('/diagnostic')
def diagnostic():
    return render_template('diagnostic.html')

@main_bp.route('/result')
def result():
    return render_template('result.html')


@main_bp.route('/lessons')
def lessons():
    # جلب جميع الدروس من قاعدة البيانات
    all_lessons = Lesson.query.order_by(Lesson.subject, Lesson.order).all()
    return render_template('lessons.html', lessons=all_lessons)