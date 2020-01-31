#!/usr/bin/python3
"""Endpoints related to Reviews"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews/', methods=['GET', 'POST'])
def reviews(place_id):
    """ Route for getting reviews data. """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        if 'user_id' not in json:
            return abort(make_response('Missing user_id', 400))
        user = storage.get('User', json.get(user_id))
        if user is None:
            return abort(404)
        if 'text' not in json:
            return abort(make_response('Missing text', 400))
        review = Review(**json)
        review.save()
        return jsonify(review.to_dict()), 201

    return jsonify([review.to_dict() for review in storage.all('Review').values()])


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review(review_id):
    """ Route for getting specific review data. """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return '{}', 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            return abort(make_response('Not a JSON', 400))
        for k, v in json.items():
            if k in ('id', 'user_id' 'place_id', 'updated_at', 'created_at'):
                continue
            setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200

    return jsonify(review.to_dict())
