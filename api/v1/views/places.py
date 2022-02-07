#!/usr/bin/python3
"""
new view for City objects that handles all default RESTFul API
actions
"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_from_cities(city_id):
    """returns the city that is part of the state
    represented with state_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        if place.city_id == city.id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Get the city identified by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def DELETE_place_id(place_id=None):
    """Delete city identified by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def POST_places(city_id):
    """creates a city only using the name
    and returns it as a dictionary"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif not data.get('user_id'):
        abort(400, "Missing name")
    else:
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        elif not data.get('name'):
            abort(404, "Missing name")
        else:
            data['city_id'] = city_id
            NewPlace = Place(**data)
            storage.new(NewPlace)
            NewPlace.save()
            return jsonify(NewPlace.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def PUT_place_id(place_id):
    """updates instance but asking for its id and returns it as a dictionary"""
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        for key, value in request_data.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(place, key, value)
        storage.save()
        result = place.to_dict()
        return jsonify(result), 200
