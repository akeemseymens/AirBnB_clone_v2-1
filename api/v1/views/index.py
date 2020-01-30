#!/usr/bin/python3
"""
Main views for the api/
"""

from flask import jsonify
from . import app_views
from models import storage


@app_views.route('/status')
def status():
    """ Get the status of the api. """
    d = {'status': 'OK'}
    return jsonify(d)


@app_views.route('/stats')
def stats():
    """ Route for getting states stats data. """
    d = {}
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    for clss in classes:
        d[clss] = storage.count(clss)
    return jsonify(d)
