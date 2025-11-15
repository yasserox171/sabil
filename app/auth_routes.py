from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import RegisterForm
from .models import Student
from . import db
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = Student.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("❌ هذا البريد الإلكتروني مسجل بالفعل!", "danger")
            return redirect(url_for('auth_bp.register'))

        hashed_password = generate_password_hash(form.password.data)
        new_student = Student(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            grade=form.grade.data
        )
        db.session.add(new_student)
        db.session.commit()

        flash("✅ تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.", "success")
        return redirect(url_for('auth_bp.login'))

    # ✅ هنا نمرّر الـ form للـ HTML
    return render_template('register.html', form=form)
