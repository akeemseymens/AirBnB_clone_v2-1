from flask import jsonify
from . import app_views

@app_views.route('/status')
def index():
    d = {'status': 'OK'}
    return jsonify(d)
