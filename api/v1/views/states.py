#!/usr/bin/python3
"""
new view for State objects that handles all default RESTFul API
actions
"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def Lists_states():
    """returns a list with all the instances of State"""
    list = []
    states = storage.all(State).values()
    for state in states:
        list.append(state.to_dict())
    return jsonify(list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def Instance_states_id(state_id):
    """returns the instance that is specified by id"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)

    return jsonify(states.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def POST_states():
    """creates instance requesting only the name
    and returns it as a dictionary"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif not data.get('name'):
        abort(400, "Missing name")
    else:
        NewState = State(**data)
        storage.new(NewState)
        NewState.save()
        return jsonify(NewState.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def PUT_states_id(state_id):
    """creates instance but asking for its id and returns it as a dictionary"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    else:
        for key, value in request_data.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(states, key, value)
        storage.save()
        result = states.to_dict()
        return jsonify(result), 200


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def DELETE_states_id(state_id=None):
    """remove instance by id and return an empty dictionary"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)

    storage.delete(states)
    storage.save()

    return jsonify({}), 200
