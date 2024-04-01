#!/usr/bin/python3
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
    new = City(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT", "DELETE", "GET"])
def city(city_id=None):
    """"""
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
     for k, v in info if k not in ["id", "update_at", "crea    ted_at"]]
    return jsonify(city.to_dict())
