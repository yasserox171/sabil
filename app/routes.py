from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user, login_user, logout_user  # ⚠️ أضف هذا
from .forms import RegisterForm, LoginForm
from .models import Lesson, User, DiagnosticTest, TestResult  # ⚠️ تغيير من Student إلى User
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
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # ⚠️ تغيير من Student إلى User
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('✅ تم تسجيل الدخول بنجاح!', 'success')
            
            # ✅ توجيه حسب الدور
            if user.role == 'teacher':
                return redirect(url_for('teacher.teacher_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('❌ البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
    
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()  # ⚠️ تغيير
        if existing_user:
            flash('❌ هذا البريد الإلكتروني مسجل بالفعل!', 'danger')
            return redirect(url_for('main.register'))
        
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(  # ⚠️ تغيير من Student إلى User
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            grade=form.grade.data,
            role='student'  # ⚠️ إضافة دور افتراضي
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash('✅ تم إنشاء الحساب بنجاح!', 'success')
        return redirect(url_for('main.dashboard'))
    
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

@main_bp.route('/dashboard')
@login_required  # ✅ أضف هذا الديكوراتور
def dashboard():
    student = current_user
    # إحصائيات حقيقية (يمكن تطويرها لاحقاً)
    completed_tests = TestResult.query.filter_by(student_id=student.id).count()
    
    student_data = {
        'username': student.username,
        'grade': student.grade,
        'completed_lessons': 3,  # مؤقت - سنطوره لاحقاً
        'completed_tests': completed_tests,
        'average_score': 85,     # مؤقت - سنطوره لاحقاً
        'learning_hours': 12     # مؤقت - سنطوره لاحقاً
    }
    return render_template('dashboard.html', student=student_data)

@main_bp.route('/logout')
def logout():
    # TODO: تنفيذ تسجيل الخروج مع Flask-Login
    flash('✅ تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('main.home'))

@main_bp.route('/submit_test/<int:test_id>', methods=['POST'])
@login_required
def submit_test(test_id):
    try:
        data = request.get_json()
        test = DiagnosticTest.query.get_or_404(test_id)
        
        # حساب النتيجة
        score = 0
        correct_answers = 0
        user_answers = {}
        total_points = 0
        
        questions = test.get_questions()
        for question in questions:
            total_points += question['points']
            
            user_answer = data.get('answers', {}).get(str(question['id']))
            user_answers[question['id']] = user_answer
            
            # التصحيح حسب نوع السؤال
            if question['type'] == 'multiple_choice':
                if user_answer and int(user_answer) == question['correct_answer']:
                    correct_answers += 1
                    score += question['points']
                    
            elif question['type'] == 'true_false':
                if user_answer and user_answer.lower() == str(question['correct_answer']).lower():
                    correct_answers += 1
                    score += question['points']
                    
            elif question['type'] == 'fill_blank':
                if user_answer and user_answer.strip().lower() == question['correct_answer'].strip().lower():
                    correct_answers += 1
                    score += question['points']
                    
            elif question['type'] == 'matching':
                # تصحيح أسئلة التوصيل
                matching_correct = 0
                total_matches = len(question['correct_matches'])
                
                for i in range(len(question['left_items'])):
                    match_key = f"question_{question['id']}_match_{i}"
                    user_match = data.get('matching_answers', {}).get(match_key)
                    
                    if user_match and f"{i}-{user_match}" in question['correct_matches']:
                        matching_correct += 1
                
                if total_matches > 0:
                    match_score = (matching_correct / total_matches) * question['points']
                    score += match_score
                    if matching_correct == total_matches:
                        correct_answers += 1
        
        # حساب النسبة المئوية
        percentage_score = (score / total_points) * 100 if total_points > 0 else 0
        
        # حفظ النتيجة
        result = TestResult(
            student_id=current_user.id,
            test_id=test_id,
            score=percentage_score,
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
            'score': percentage_score,
            'correct_answers': correct_answers,
            'total_questions': len(questions),
            'total_points': total_points,
            'earned_points': score
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})