#!/usr/bin/python3
"""Endpoints related to Places"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/places/', methods=['GET', 'POST'])
def places():
    """ Route for getting places data. """
    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        if 'name' not in json:
            return abort(make_response('Missing name', 400))
        place = Place(**json)
        place.save()
        return jsonify(place.to_dict()), 201

    return jsonify([place.to_dict() for place in storage.all('Place').values()])


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place(place_id):
    """ Route for getting specific place data. """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return '{}', 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        for k, v in json.items():
            if k in ('id', 'updated_at', 'created_at'):
                continue
            setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200

    return jsonify(place.to_dict())
