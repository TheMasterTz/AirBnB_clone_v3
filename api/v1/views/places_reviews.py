#!/usr/bin/python3
"""
new view for review objects that handles all default RESTFul API
actions
"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/api/v1/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews_from_place(place_id):
    """returns the review that is part of the place
    represented with place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews_list = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place.id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Get the review identified by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def DELETE_review_id(review_id=None):
    """Delete review identified by review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def POST_review(place_id):
    """creates a review only using the name
    and returns it as a dictionary"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif not data.get('user_id'):
        abort(400, "Missing user_id")
    elif not data.get('text'):
        abort(400, "Missing text")
    else:
        data['place_id'] = place_id
        user_id = data.get('user_id')
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        data['user_id'] = user_id
        Newreview = Review(**data)
        storage.new(Newreview)
        Newreview.save()
        return jsonify(Newreview.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def PUT_review_id(review_id):
    """updates instance but asking for its id and returns it as a dictionary"""
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        for key, value in request_data.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(review, key, value)
        storage.save()
        result = review.to_dict()
        return jsonify(result), 200
