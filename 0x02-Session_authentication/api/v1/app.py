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

if 'AUTH_TYPE' in os.environ:
    if os.environ['AUTH_TYPE'] == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    if os.environ['AUTH_TYPE'] == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.before_request
def before_request():
    """ runs before every request is made"""
    if auth is None:
        return None

    allowed_paths = [
        '/api/v1/status',
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
        ]

    if request.path not in allowed_paths:
        if not auth.require_auth(request.path, allowed_paths):
            abort(401)

        if auth.authorization_header(request) and\
           auth.session_cookie(request) is None:
            return None, abort(401)

        if auth.session_cookie(request) is None:
            return None, abort(401)

        request.current_user = auth.current_user(request)
        if request.current_user is None:
            abort(403)


# Unauthorized
@app.errorhandler(401)
def unauthorized(error) -> str:
    """ unauthorized handler """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.route('/api/v1/unauthorized')
def custom_401() -> str:
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
