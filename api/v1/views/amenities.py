#!/usr/bin/python3
"""
new view for Amenity objects that handles all default RESTFul API
actions
"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def Lists_amenitys():
    """returns a list with all the instances of amenity"""
    list = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def Instance_amenitys_id(amenity_id):
    """returns the instance that is specified by id"""
    amenitys = storage.get(Amenity, amenity_id)
    if amenitys is None:
        abort(404)

    return jsonify(amenitys.to_dict())


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def POST_amenitys():
    """creates instance requesting only the name
    and returns it as a dictionary"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif not data.get('name'):
        abort(400, "Missing name")
    else:
        NewAmenity = Amenity(**data)
        storage.new(NewAmenity)
        NewAmenity.save()
        return jsonify(NewAmenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def PUT_amenitys_id(amenity_id):
    """creates instance but asking for its id and returns it as a dictionary"""
    amenitys = storage.get(Amenity, amenity_id)
    if amenitys is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    else:
        for key, value in request_data.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(amenitys, key, value)
        storage.save()
        result = amenitys.to_dict()
        return jsonify(result), 200


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def DELETE_Amenitys_id(amenity_id=None):
    """remove instance by id and return an empty dictionary"""
    Amenitys = storage.get(Amenity, amenity_id)
    if Amenitys is None:
        abort(404)

    storage.delete(Amenitys)
    storage.save()

    return jsonify({}), 200
