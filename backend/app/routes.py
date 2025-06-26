from flask import Blueprint, request, jsonify, abort
from . import db
from .models import Quiz, Question, Choice, Participant
import random
import string

bp = Blueprint('api', __name__)

def _generate_short_code(length=6):
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not Quiz.query.filter_by(short_code=code).first():
            return code

@bp.route('/join/<short_code>', methods=['POST'])
def join(short_code):
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    quiz = Quiz.query.filter_by(short_code=short_code).first_or_404()
    participant = Participant(name=name, quiz=quiz)
    db.session.add(participant)
    db.session.commit()
    return jsonify({'participant_id': participant.id})


@bp.route('/api/quizzes', methods=['GET'])
def list_quizzes():
    """Return paginated list of quizzes."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pagination = Quiz.query.paginate(page=page, per_page=per_page, error_out=False)
    quizzes = [
        {
            'id': q.id,
            'title': q.title,
            'description': q.description,
            'short_code': q.short_code,
        }
        for q in pagination.items
    ]
    return jsonify({'quizzes': quizzes, 'total': pagination.total})


@bp.route('/api/quizzes', methods=['POST'])
def create_quiz():
    """Create a new quiz."""
    data = request.get_json() or {}
    title = data.get('title')
    if not title:
        return jsonify({'error': 'title is required'}), 400
    description = data.get('description')
    quiz = Quiz(title=title, description=description, short_code=_generate_short_code())
    db.session.add(quiz)
    db.session.commit()
    return jsonify({'id': quiz.id, 'short_code': quiz.short_code}), 201


@bp.route('/api/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get quiz details including questions."""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = [
        {
            'id': q.id,
            'text': q.text,
            'qtype': q.qtype,
            'time_limit': q.time_limit,
            'media_url': q.media_url,
            'order': q.order,
            'choices': [
                {'id': c.id, 'text': c.text, 'is_correct': c.is_correct}
                for c in q.choices
            ],
        }
        for q in quiz.questions
    ]
    return jsonify(
        {
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'short_code': quiz.short_code,
            'questions': questions,
        }
    )


@bp.route('/api/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    """Update quiz title or description."""
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json() or {}
    if 'title' in data and not data['title']:
        return jsonify({'error': 'title cannot be empty'}), 400
    quiz.title = data.get('title', quiz.title)
    quiz.description = data.get('description', quiz.description)
    db.session.commit()
    return jsonify({'id': quiz.id})


@bp.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """Delete quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({'status': 'deleted'})


@bp.route('/api/quizzes/<int:quiz_id>/questions', methods=['POST'])
def create_question(quiz_id):
    """Create question for a quiz."""
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json() or {}
    text = data.get('text')
    qtype = data.get('qtype')
    if not text or not qtype:
        return jsonify({'error': 'text and qtype are required'}), 400
    question = Question(
        quiz=quiz,
        text=text,
        qtype=qtype,
        time_limit=data.get('time_limit', 30),
        media_url=data.get('media_url'),
        order=data.get('order'),
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'id': question.id}), 201


@bp.route('/api/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """Update a question."""
    question = Question.query.get_or_404(question_id)
    data = request.get_json() or {}
    if 'text' in data and not data['text']:
        return jsonify({'error': 'text cannot be empty'}), 400
    question.text = data.get('text', question.text)
    question.qtype = data.get('qtype', question.qtype)
    question.time_limit = data.get('time_limit', question.time_limit)
    question.media_url = data.get('media_url', question.media_url)
    db.session.commit()
    return jsonify({'id': question.id})


@bp.route('/api/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """Delete question."""
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'status': 'deleted'})


@bp.route('/api/questions/<int:question_id>/choices', methods=['POST'])
def add_choice(question_id):
    """Add choice to question."""
    question = Question.query.get_or_404(question_id)
    data = request.get_json() or {}
    text = data.get('text')
    if text is None:
        return jsonify({'error': 'text is required'}), 400
    choice = Choice(
        question=question,
        text=text,
        is_correct=data.get('is_correct', False),
    )
    db.session.add(choice)
    db.session.commit()
    return jsonify({'id': choice.id}), 201


@bp.route('/api/choices/<int:choice_id>', methods=['PUT'])
def update_choice(choice_id):
    """Update a choice."""
    choice = Choice.query.get_or_404(choice_id)
    data = request.get_json() or {}
    if 'text' in data and data['text'] is None:
        return jsonify({'error': 'text cannot be null'}), 400
    choice.text = data.get('text', choice.text)
    if 'is_correct' in data:
        choice.is_correct = data['is_correct']
    db.session.commit()
    return jsonify({'id': choice.id})


@bp.route('/api/choices/<int:choice_id>', methods=['DELETE'])
def delete_choice(choice_id):
    """Delete a choice."""
    choice = Choice.query.get_or_404(choice_id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({'status': 'deleted'})

@bp.route('/api/quizzes/<int:quiz_id>/start_session', methods=['POST'])
def start_session(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    # This would trigger a SocketIO event in real implementation
    return jsonify({'status': 'started', 'quiz_id': quiz.id})
