from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .models import User, Lesson, DiagnosticTest, TestResult
from .teacher_forms import UniversalQuestionForm, LessonForm, TestForm
from . import db
import json

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

# التحقق من صلاحيات المدرب
def teacher_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('❌ ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def teacher_dashboard():
    # إحصائيات المدرب
    stats = {
        'total_lessons': Lesson.query.filter_by(created_by=current_user.id).count(),
        'published_lessons': Lesson.query.filter_by(created_by=current_user.id, is_published=True).count(),
        'total_tests': DiagnosticTest.query.filter_by(created_by=current_user.id).count(),
        'published_tests': DiagnosticTest.query.filter_by(created_by=current_user.id, is_published=True).count(),
        'total_students': User.query.filter_by(role='student').count(),
        'total_results': TestResult.query.count()
    }
    
    return render_template('teacher/dashboard.html', stats=stats)
def redirect_old_dashboard():
    """إعادة توجيه للروابط القديمة"""
    return redirect(url_for('teacher.teacher_dashboard'))

@teacher_bp.route('/lessons')
@login_required
@teacher_required
def teacher_lessons_management():
    lessons = Lesson.query.filter_by(created_by=current_user.id).order_by(Lesson.created_at.desc()).all()
    return render_template('teacher/lessons.html', lessons=lessons)

@teacher_bp.route('/lessons/new', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_new_lesson():
    form = LessonForm()
    
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            description=form.description.data,
            subject=form.subject.data,
            grade_level=form.grade_level.data,
            duration=form.duration.data,
            video_url=form.video_url.data,
            document_url=form.document_url.data,
            is_published=form.is_published.data,
            created_by=current_user.id
        )
        
        db.session.add(lesson)
        db.session.commit()
        
        flash('✅ تم إنشاء الدرس بنجاح!', 'success')
        return redirect(url_for('teacher.teacher_lessons_management'))
    
    return render_template('teacher/lesson_form.html', form=form, title='إنشاء درس جديد')

@teacher_bp.route('/lessons/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # التحقق من ملكية الدرس
    if lesson.created_by != current_user.id:
        flash('❌ ليس لديك صلاحية لتعديل هذا الدرس', 'danger')
        return redirect(url_for('teacher.teacher_lessons_management'))
    
    form = LessonForm(obj=lesson)
    
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.description = form.description.data
        lesson.subject = form.subject.data
        lesson.grade_level = form.grade_level.data
        lesson.duration = form.duration.data
        lesson.video_url = form.video_url.data
        lesson.document_url = form.document_url.data
        lesson.is_published = form.is_published.data
        
        db.session.commit()
        flash('✅ تم تحديث الدرس بنجاح!', 'success')
        return redirect(url_for('teacher.teacher_lessons_management'))
    
    return render_template('teacher/lesson_form.html', form=form, title='تعديل الدرس', lesson=lesson)

@teacher_bp.route('/tests')
@login_required
@teacher_required
def teacher_tests_management():
    tests = DiagnosticTest.query.filter_by(created_by=current_user.id).order_by(DiagnosticTest.created_at.desc()).all()
    return render_template('teacher/tests.html', tests=tests)

@teacher_bp.route('/tests/new', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_new_test():
    form = TestForm()
    
    if form.validate_on_submit():
        test = DiagnosticTest(
            title=form.title.data,
            description=form.description.data,
            subject=form.subject.data,
            grade_level=form.grade_level.data,
            time_limit=form.time_limit.data,
            is_published=form.is_published.data,
            created_by=current_user.id,
            questions='[]'  # قائمة أسئلة فارغة
        )
        
        db.session.add(test)
        db.session.commit()
        
        flash('✅ تم إنشاء الاختبار بنجاح!', 'success')
        return redirect(url_for('teacher.teacher_tests_management'))
    
    return render_template('teacher/test_form.html', form=form, title='إنشاء اختبار جديد')

@teacher_bp.route('/tests/<int:test_id>/questions', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_manage_questions(test_id):
    test = DiagnosticTest.query.get_or_404(test_id)
    
    # التحقق من ملكية الاختبار
    if test.created_by != current_user.id:
        flash('❌ ليس لديك صلاحية لإدارة هذا الاختبار', 'danger')
        return redirect(url_for('teacher.teacher_tests_management'))
    
    form = UniversalQuestionForm()
    
    if form.validate_on_submit():
        questions = test.get_questions()
        
        # إنشاء كائن السؤال حسب النوع
        new_question = {
            'id': len(questions) + 1,
            'type': form.question_type.data,
            'question': form.question.data,
            'points': form.points.data,
            'explanation': form.explanation.data
        }
        
        # إضافة البيانات حسب نوع السؤال
        if form.question_type.data == 'multiple_choice':
            new_question.update({
                'options': [
                    form.option1.data,
                    form.option2.data,
                    form.option3.data,
                    form.option4.data
                ],
                'correct_answer': int(form.correct_choice.data)
            })
            
        elif form.question_type.data == 'true_false':
            new_question.update({
                'correct_answer': form.correct_bool.data == 'True'
            })
            
        elif form.question_type.data == 'fill_blank':
            new_question.update({
                'correct_answer': form.correct_text.data,
                'hint': form.hint_text.data
            })
            
        elif form.question_type.data == 'matching':
            new_question.update({
                'left_items': [item.strip() for item in form.left_items.data.split('\n') if item.strip()],
                'right_items': [item.strip() for item in form.right_items.data.split('\n') if item.strip()],
                'correct_matches': [match.strip() for match in form.correct_matches.data.split('\n') if match.strip()]
            })
        
        questions.append(new_question)
        test.set_questions(questions)
        db.session.commit()
        
        flash('✅ تم إضافة السؤال بنجاح!', 'success')
        return redirect(url_for('teacher.teacher_manage_questions', test_id=test_id))
    
    questions = test.get_questions()
    return render_template('teacher/questions.html', test=test, form=form, questions=questions)

@teacher_bp.route('/tests/<int:test_id>/questions/<int:question_id>/delete')
@login_required
@teacher_required
def teacher_delete_question(test_id, question_id):
    test = DiagnosticTest.query.get_or_404(test_id)
    
    if test.created_by != current_user.id:
        flash('❌ ليس لديك صلاحية لحذف هذا السؤال', 'danger')
        return redirect(url_for('teacher.teacher_tests_management'))
    
    questions = test.get_questions()
    questions = [q for q in questions if q['id'] != question_id]
    
    # إعادة ترقيم الأسئلة
    for i, question in enumerate(questions, 1):
        question['id'] = i
    
    test.set_questions(questions)
    db.session.commit()
    
    flash('✅ تم حذف السؤال بنجاح!', 'success')
    return redirect(url_for('teacher.teacher_manage_questions', test_id=test_id))

@teacher_bp.route('/results')
@login_required
@teacher_required
def teacher_view_results():
    # نتائج جميع الاختبارات التي أنشأها المدرب
    results = TestResult.query.join(DiagnosticTest).filter(
        DiagnosticTest.created_by == current_user.id
    ).order_by(TestResult.completed_at.desc()).all()
    
    return render_template('teacher/results.html', results=results)

@teacher_bp.route('/students')
@login_required
@teacher_required
def teacher_view_students():
    students = User.query.filter_by(role='student').all()
    return render_template('teacher/students.html', students=students)