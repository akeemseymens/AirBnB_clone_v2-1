#!/usr/bin/python3
"""Endpoints related to States"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """ Route for getting states data. """
    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        if 'name' not in json:
            return abort(make_response('Missing name', 400))
        state = State(**json)
        state.save()
        return jsonify(state.to_dict()), 201

    return jsonify([state.to_dict() for state in storage.all('State').values()])


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    """ Route for getting specific state data. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return '{}', 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        for k, v in json.items():
            if k in ('id', 'updated_at', 'created_at'):
                continue
            setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200

    return jsonify(state.to_dict())
