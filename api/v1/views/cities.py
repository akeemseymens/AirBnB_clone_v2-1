#!/usr/bin/python3
"""
Endpoints related to Cities.
"""

from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def state_cities(state_id):
    """ Route for getting specific state data. """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            return 'Not a JSON', 400
        if 'name' not in json:
            return 'Missing name', 400
        city = City(**json)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """ Route for specific cities. """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return '{}', 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            return 'Not a JSON', 400
        for k, v in json.items():
            if k in ('id', 'state_id', 'updated_at', 'created_at'):
                continue
            setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200

    return jsonify(city.to_dict())
