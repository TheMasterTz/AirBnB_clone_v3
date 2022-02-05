#!/usr/bin/python3
"""index module"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status_check():
    """Returns the status of the app"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def count_objs():
    """Returns the count of objects"""
    result = {}
    classes = {'amenities': 'Amenity', 'cities': 'City', 'places': 'Place',
               'reviews': 'Review','states': 'State', 'users': 'User'}
    for key, value in classes.items():
        result[key] = storage.count(value)
    return jsonify(result)
    