#!/usr/bin/python3
"""Place blueprint view routes"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def places(city_id=None):
    """defines POST and GET request method
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "GET":
        return jsonify(
                [place.to_dict() for place in city.places]
                )
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    if not info.get("user_id"):
        abort(400, "Missing user_id")
    if not storage.get(User, info.get("user_id")):
        abort(404)
    if not info.get("name"):
        abort(400, "Missing name")
    info["city_id"] = city_id
    new = City(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT", "DELETE", "GET"])
def place(place_id=None):
    """update, delete or get specific place by the id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({})
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    [setattr(place, k, v)
     for k, v in info.items()
     if k not in ["id", "update_at", "created_at"]]
    place.save()
    return jsonify(place.to_dict())
