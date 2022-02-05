#!/usr/bin/python3
"""
new view for State objects that handles all default RESTFul API
actions
"""

from models import storage
from flask import jsonify, abort
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
