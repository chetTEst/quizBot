from app.models import Quiz, Question, Choice, Participant, Answer
from app import db


def test_quiz_creation(app):
    quiz = Quiz(title='Sample', description='desc', short_code='ABC123')
    db.session.add(quiz)
    db.session.commit()
    assert quiz.id is not None
    assert quiz.created_at is not None
    assert quiz.updated_at is not None


def test_question_relationship(app):
    quiz = Quiz(title='q', description='d', short_code='CODE1')
    db.session.add(quiz)
    db.session.commit()
    q = Question(quiz=quiz, text='Q', qtype='tf')
    db.session.add(q)
    db.session.commit()
    assert q.quiz_id == quiz.id


def test_choice_relationship(app):
    quiz = Quiz(title='q', description='d', short_code='CODE2')
    db.session.add(quiz)
    db.session.commit()
    ques = Question(quiz=quiz, text='Q', qtype='tf')
    db.session.add(ques)
    db.session.commit()
    ch = Choice(question=ques, text='A', is_correct=True)
    db.session.add(ch)
    db.session.commit()
    assert ch.question_id == ques.id

