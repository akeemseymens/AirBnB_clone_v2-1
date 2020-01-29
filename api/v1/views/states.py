from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
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


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
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
        for k, v is json.items():
            if k in ('id', 'updated_at', 'created_at'):
                pass
            state[k] = v
        return state, 200

    return jsonify(state.to_dict())
