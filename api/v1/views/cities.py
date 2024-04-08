#!/usr/bin/python3
"""state blueprint view routes"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def cities(state_id=None):
    """defines POST and GET request method
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "GET":
        return jsonify(
                [city.to_dict() for city in state.cities]
                )
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    if not info.get("name"):
        abort(400, "Missing name")
    info["state_id"] = state_id
    print(info)
    new = City(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT", "DELETE", "GET"])
def city(city_id=None):
    """update, delete or get specific city by the id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        city.delete()
        storage.save()
        return jsonify({})
    info = request.get_json()
    if not info:
        abort(400, "Not JSON")
    [setattr(city, k, v)
     for k, v in info.items()
     if k not in ["id", "update_at", "created_at"]]
    city.save()
    return jsonify(city.to_dict())
