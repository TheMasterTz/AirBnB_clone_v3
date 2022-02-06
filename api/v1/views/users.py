#!/usr/bin/python3
"""
new view for user objects that handles all default RESTFul API
actions
"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def Lists_users():
    """returns a list with all the instances of user"""
    list = []
    users = storage.all(User).values()
    for user in users:
        list.append(user.to_dict())
    return jsonify(list)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def Instance_users_id(user_id):
    """returns the instance that is specified by id"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)

    return jsonify(users.to_dict())


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def POST_users():
    """creates instance requesting only the name
    and returns it as a dictionary"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif not data.get('email'):
        abort(400, "Missing email")
    elif not data.get('password'):
        abort(400, "Missing password")
    else:
        NewUser = User(**data)
        storage.new(NewUser)
        NewUser.save()
        return jsonify(NewUser.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def PUT_users_id(user_id):
    """creates instance but asking for its id and returns it as a dictionary"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    else:
        for key, value in request_data.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(users, key, value)
        storage.save()
        result = users.to_dict()
        return jsonify(result), 200


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def DELETE_users_id(user_id=None):
    """remove instance by id and return an empty dictionary"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)

    storage.delete(users)
    storage.save()

    return jsonify({}), 200
