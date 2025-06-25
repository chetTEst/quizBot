from datetime import datetime
from sqlalchemy import Enum
from . import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    short_code = db.Column(db.String(8), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    qtype = db.Column(Enum('tf', 'single', 'text', 'numeric', name='qtype'), nullable=False)
    time_limit = db.Column(db.Integer, default=30)
    media_url = db.Column(db.String(255))
    order = db.Column(db.Integer)
    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean, default=False)
    question = db.relationship('Question', backref=db.backref('choices', lazy=True))

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    session_id = db.Column(db.String(36), unique=True)
    score = db.Column(db.Integer, default=0)
    quiz = db.relationship('Quiz', backref=db.backref('participants', lazy=True))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    value = db.Column(db.Text)
    correct = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
