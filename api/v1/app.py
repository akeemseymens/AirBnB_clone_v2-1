#!/usr/bin/python3
"""
Create a Flask app.
"""

import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"app_views": "*"}})

@app.teardown_appcontext
def teardown_db(e):
    """Close the database connection"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """404 page"""
    d = {'error': 'Not found'}
    return jsonify(d), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
