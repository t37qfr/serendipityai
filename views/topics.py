import json
from flask import Blueprint, make_response, request
from serializers.topics import TopicSerializer
from queries.topics import TopicQuery

topics = Blueprint('topics', __name__)

@topics.route('/topics/', methods=['GET'])
def list():
    topic_name = request.args.get('name', None)
    if topic_name:
        # this is a quick dirty solution to make possible a multi word search
        # a more complex solution would be to encode the value to a url param and decode here
        topic_name = topic_name.replace('+', ' ')

    data = TopicQuery().list(name=topic_name)

    response = [TopicSerializer(d).to_dict() for d in data]

    return json.dumps({'topics': response})


@topics.route('/topics/<id>/', methods=['GET'])
def get(id):
    if not id:
        return make_response({'msg': 'Invalid Request'}, 400)

    data = TopicQuery().get(id=id)

    if not data:
        return make_response({'msg': 'Not Found'}, 404)

    response = TopicSerializer(data).to_dict()

    return json.dumps(response)


@topics.route('/topics/', methods=['POST'])
def create():
    new_topic = request.json

    user_id = request.headers.get('user_id')

    data = TopicQuery(user_id=user_id).create(new_topic)

    response = TopicSerializer(data).to_dict()

    return json.dumps({'topic': response}), 201


@topics.route('/topics/<id>/', methods=['DELETE'])
def delete(id):
    if not id:
        return make_response({'msg': 'Invalid Request'}, 400)

    user_id = request.headers.get('user_id')

    response = TopicQuery(user_id=user_id).delete(id)

    if not response:
        return make_response({'msg': 'Not Found'}, 404)

    return {'msg', 'deleted'}, 204


@topics.route('/topics/<id>', methods=['PUT'])
def update(id):
    if not id:
        return make_response({'msg': 'Invalid Request'}, 400)

    user_id = request.headers.get('user_id')

    topic = request.json

    data = TopicQuery(user_id=user_id).update(id, topic)

    if not data:
        return make_response({'msg': 'Not Found'}, 404)

    response = TopicSerializer(data).to_dict()

    return json.dumps(response), 200

