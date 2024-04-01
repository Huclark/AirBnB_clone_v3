#!/usr/bin/python3
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def cities(state_id):
    """defines POST and GET request method
    POST: 
    """
