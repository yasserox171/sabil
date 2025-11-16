from . import db
from datetime import datetime
import json

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    grade = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(300))
    document_url = db.Column(db.String(300))
    subject = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(20))
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DiagnosticTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    grade_level = db.Column(db.String(50), nullable=False)  # ⚠️ هذا الحقل كان ناقصاً
    description = db.Column(db.Text)
    time_limit = db.Column(db.Integer)
    questions = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_questions(self):
        return json.loads(self.questions) if self.questions else []
    
    def set_questions(self, questions_list):
        self.questions = json.dumps(questions_list)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('diagnostic_test.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)
    answers = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref='test_results')
    test = db.relationship('DiagnosticTest', backref='results')
    
    def get_answers(self):
        return json.loads(self.answers) if self.answers else {}
    
    def set_answers(self, answers_dict):
        self.answers = json.dumps(answers_dict)