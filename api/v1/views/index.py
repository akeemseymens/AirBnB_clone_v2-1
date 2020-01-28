from flask import jsonify
from . import app_views
from models import storage


@app_views.route('/status')
def status():
    d = {'status': 'OK'}
    return jsonify(d)


@app_views.route('/stats')
def stats():
    d = {}
    classes = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    for clss in classes:
        d[clss] = storage.count(clss)
    return jsonify(d)
