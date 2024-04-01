#!/usr/bin/python3
"""flask app"""
from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Response with JSON-formatted 404 status code."""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_storage(exc):
    """Closes the storage session after every request."""
    storage.close()


if __name__ == "__main__":
    app.run(
      host=getenv("HBNB_API_HOST", default="0.0.0.0"),
      port=getenv("HBNB_API_PORT", default="5000"),
      threaded=True
      )
app.url_map.strict_slashes = False
