#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv('AUTH_TYPE'):
    auth = getenv('AUTH_TYPE')
else:
    auth = 'none'

# authorising
if auth and isinstance(auth, type):
    from api.v1.auth import Auth
    auth = Auth()


excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

@app.before_request
def before_request():
    if auth is None:
        return
    else:
        auth = None
    
    path = request.path
    if path not in excluded_paths and auth.require_auth(path, excluded_paths):
        if auth.authorization_header(request) is None:
            return abort(401, description="Unauthorized")
        
        if auth.current_user(request) is None:
            return abort(403, description="Forbidden")


# Unauthorized
@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized handler """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response

@app.route('/api/v1/unauthorized')
def  custom_401() -> str:
    """ Custom 401 error message route """
    return abort(401)

# Forbiden
@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden access handler """
    return jsonify({"error": "Forbidden"}), 403

@app.route('/api/v1/forbidden')
def custom_403() -> str:
    """ Custom 403 error message route """
    return abort(403)


# not found
@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.debug = True
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
