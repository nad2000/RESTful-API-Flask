from functools import wraps
from flask import request, jsonify


def app_required(f):
    @wraps(f)
    def decorated_funcion(*args, **kwargs):
        app_id = request.headers.get("X-APP-ID")
        if not app_id:
            return jsonify({}), 403
        app_secret =request.headers.get("X-APP-SECRET")
        print(app_id, app_id)
        if not (app_id == "xxx" and app_secret = "123"):
            return jsonify({}), 403
        return f(*args, **kwargs)
    return decorated_function


