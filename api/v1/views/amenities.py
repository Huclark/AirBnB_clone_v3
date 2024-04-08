#!/usr/bin/python3
"""Define amenity blueprint view for RESTful API"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/<amenity_id>", methods=["GET", "PUT", "DELETE"])
def amenities(amenity_id=None):
    """Rtrieve, update or delete amenities with amenity id provided"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == "GET":
        return jsoniify(amenity.to_dict())
    if request.method == "DELETE":
        amenity.delete()
        storage.save()
        return jsonify({})
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ["created_at", "id", "updated_at"]:
            setattr(amenity, k, v)
            amenity.save()
    return jsonify(amenity.to_dict())


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """define amenity blueprint to create new amenity"""
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    if not info.get("name"):
        abort(400, "Missing name")
    new = Amenity(**info)
    new.save()
    return jsonify(new.to_dict())
