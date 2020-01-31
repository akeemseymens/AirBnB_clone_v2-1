#!/usr/bin/python3
"""Endpoints related to Users"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET', 'POST'])
def users():
    """ Route for getting users data. """
    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        if 'email' not in json:
            return abort(make_response('Missing email', 400))
        if 'password' not in json:
            return abort(make_response('Missing password', 400))
        user = User(**json)
        user.save()
        return jsonify(user.to_dict()), 201

    return jsonify([user.to_dict() for user in storage.all('User').values()])


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    """ Route for getting specific user data. """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return '{}', 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        for k, v in json.items():
            if k in ('id', 'email', 'updated_at', 'created_at'):
                continue
            setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200

    return jsonify(user.to_dict())
