from .models import Participant, Question
from . import db

def register_socketio_events(socketio):
    @socketio.on('submit_answer')
    def handle_submit(data):
        participant_id = data.get('participant_id')
        question_id = data.get('question_id')
        value = data.get('value')
        # TODO: validate and update score
        pass
