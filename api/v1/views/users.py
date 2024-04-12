#!/usr/bin/python3
"""Users blueprint view for flask app"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def users():
    """user blueprint route that get the list of all user
    and create new user
    """
    if request.method == "GET":
        return jsonify([
            user.to_dict() for user in storage.all("User").values()
            ])
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    if not info.get("email"):
        abort(400, "Missing email")
    if not info.get("password"):
        abort(400, "Missing password")
    new = User(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id=None):
    """define user view blueprint method to:
    DELETE:  a specific user whose id is provided.
    GET: a specific user whose id is provided.
    UPDATE: a specifi user whose id is provided
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({})
    info = request.get_json(silent=True)
    if not info:
        abort(400, "Not a JSON")
    for k, v in info.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict())
