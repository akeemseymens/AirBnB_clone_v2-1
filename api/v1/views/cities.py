#!/usr/bin/python3
"""
Endpoints related to Cities.
"""

from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET', 'POST'])
def cities():
    """ Route for getting cities data. """
    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            return 'Not a JSON', 400
        if 'name' not in json:
            return 'Missing name', 400
        state = State(**json)
        storage.new(state)
        return state, 201

    return jsonify(storage.all('State'))


@app_views.route('/states/<state_id>/cities', methods=['GET', 'DELETE', 'PUT'])
def state_cities(state_id):
    """ Route for getting specific state data. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(state)
        return '{}', 200

    if request.method == 'PUT':
        json = request.json()
        if json is None:
            return 'Not a JSON', 400
        for k, v in json.items():
            if k in ('id', 'updated_at', 'created_at'):
                pass
            state[k] = v
        return state, 200

    return jsonify(state.cities)
