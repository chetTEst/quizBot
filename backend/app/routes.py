from flask import Blueprint, request, jsonify
from . import db
from .models import Quiz, Participant

bp = Blueprint('api', __name__)

@bp.route('/join/<short_code>', methods=['POST'])
def join(short_code):
    name = request.json.get('name')
    quiz = Quiz.query.filter_by(short_code=short_code).first_or_404()
    participant = Participant(name=name, quiz=quiz)
    db.session.add(participant)
    db.session.commit()
    return jsonify({'participant_id': participant.id})

@bp.route('/api/quizzes/<int:quiz_id>/start_session', methods=['POST'])
def start_session(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    # This would trigger a SocketIO event in real implementation
    return jsonify({'status': 'started', 'quiz_id': quiz.id})
