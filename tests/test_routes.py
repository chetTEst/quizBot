import json
from app.models import Quiz, Question, Choice
from app import db


def create_quiz(client, title='Quiz 1'):
    res = client.post('/api/quizzes', json={'title': title, 'description': 'd'})
    assert res.status_code == 201
    return res.get_json()['id']


def test_create_get_update_delete_quiz(client):
    qid = create_quiz(client)
    # get
    res = client.get(f'/api/quizzes/{qid}')
    assert res.status_code == 200
    data = res.get_json()
    assert data['title'] == 'Quiz 1'

    # update
    res = client.put(f'/api/quizzes/{qid}', json={'title': 'New'})
    assert res.status_code == 200
    res = client.get(f'/api/quizzes/{qid}')
    assert res.get_json()['title'] == 'New'

    # delete
    res = client.delete(f'/api/quizzes/{qid}')
    assert res.status_code == 200
    res = client.get(f'/api/quizzes/{qid}')
    assert res.status_code == 404


def test_question_crud(client):
    qid = create_quiz(client)
    res = client.post(f'/api/quizzes/{qid}/questions', json={'text': 'Q?', 'qtype': 'tf'})
    assert res.status_code == 201
    ques_id = res.get_json()['id']

    res = client.put(f'/api/questions/{ques_id}', json={'text': 'New?', 'time_limit': 10})
    assert res.status_code == 200

    res = client.delete(f'/api/questions/{ques_id}')
    assert res.status_code == 200


def test_choice_crud(client):
    qid = create_quiz(client)
    res = client.post(f'/api/quizzes/{qid}/questions', json={'text': 'Q?', 'qtype': 'single'})
    question_id = res.get_json()['id']

    res = client.post(f'/api/questions/{question_id}/choices', json={'text': 'A', 'is_correct': True})
    assert res.status_code == 201
    choice_id = res.get_json()['id']

    res = client.put(f'/api/choices/{choice_id}', json={'text': 'B'})
    assert res.status_code == 200

    res = client.delete(f'/api/choices/{choice_id}')
    assert res.status_code == 200


def test_join_requires_name(client):
    qid = create_quiz(client)
    quiz = Quiz.query.get(qid)
    res = client.post(f'/join/{quiz.short_code}', json={})
    assert res.status_code == 400
    assert 'error' in res.get_json()

