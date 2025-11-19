from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .forms import RegisterForm, LoginForm
from .models import Lesson, Student, DiagnosticTest, TestResult
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

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






@main_bp.route('/result')
def result():
    return render_template('result.html')


@main_bp.route('/lessons')
def lessons():
    # جلب جميع الدروس من قاعدة البيانات
    all_lessons = Lesson.query.order_by(Lesson.subject, Lesson.order).all()
    return render_template('lessons.html', lessons=all_lessons)

@main_bp.route('/diagnostic')
def diagnostic():
    # جلب جميع الاختبارات
    all_tests = DiagnosticTest.query.filter_by(is_active=True).all()
    
    # جلب نتائج الطالب (للعرض فقط - سنضيف النظام لاحقاً)
    test_results = {}
    
    return render_template('diagnostic.html', tests=all_tests, test_results=test_results)

@main_bp.route('/take_test/<int:test_id>')
def take_test(test_id):
    test = DiagnosticTest.query.get_or_404(test_id)
    return render_template('take_test.html', test=test)

@main_bp.route('/test_result/<int:result_id>')
def test_result(result_id):
    result = TestResult.query.get_or_404(result_id)
    return render_template('test_result.html', result=result)

# API لتسجيل نتائج الاختبار
@main_bp.route('/submit_test/<int:test_id>', methods=['POST'])
def submit_test(test_id):
    try:
        data = request.get_json()
        test = DiagnosticTest.query.get_or_404(test_id)
        
        # حساب النتيجة
        score = 0
        correct_answers = 0
        user_answers = {}
        
        questions = test.get_questions()
        for question in questions:
            user_answer = data.get(str(question['id']))
            user_answers[question['id']] = user_answer
            
            if user_answer == question['correct_answer']:
                correct_answers += 1
                score += question['points']
        
        # حفظ النتيجة (لنستخدم طالب افتراضي للاختبار)
        student = Student.query.first()  # أول طالب في قاعدة البيانات
        
        result = TestResult(
            student_id=student.id,
            test_id=test_id,
            score=score,
            total_questions=len(questions),
            correct_answers=correct_answers,
            time_taken=data.get('time_taken', 0)
        )
        result.set_answers(user_answers)
        
        db.session.add(result)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'result_id': result.id,
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': len(questions)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main_bp.route('/dashboard')
def dashboard():
    # في المستقبل، سنمرر بيانات حقيقية من قاعدة البيانات
    student_data = {
        'username': 'طالب Focus',
        'grade': 'الإعدادي 1',
        'completed_lessons': 3,
        'completed_tests': 2,
        'average_score': 85,
        'learning_hours': 12
    }
    return render_template('dashboard.html', student=student_data)

@main_bp.route('/logout')
def logout():
    # TODO: تنفيذ تسجيل الخروج مع Flask-Login
    flash('✅ تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('main.home'))