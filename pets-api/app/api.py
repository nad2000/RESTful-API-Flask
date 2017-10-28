import uuid
from datetime import datetime, timedelta

import bcrypt
from flask import abort, jsonify, request
from flask.views import MethodView

from app.models import Access, App


class AppAPI(MethodView):

    def __init__(self):
        if not request.json:
            abort(400)
        super().__init__()

    def post(self):

        if not "app-id" in request.json or not "app-secret" in request.json:
            return jsonify({"error": {"code": "MISSING_APP_ID_OR_APP_SECRET"}}), 400
        app_id=request.json.get("app-id")
        existing_app = App.objects.filter(app_id=app_id).first()
        if existing_app:
            return jsonify({"error": {"code": "APP_ID_ALREADY_EXISTS"}}), 400
        else:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(request.json.get("app-secret"), salt)
            App(app_id=app_id, app_secret =hashed_password).save()
            return jsonify({"result": "ok"}), 201


class AccessAPI(MethodView):

    def __init__(self):
        if not request.json:
            abort(400)
        super().__init__()

    def post(self):

        if not "app-id" in request.json or not "app-secret" in request.json:
            return jsonify({"error": {"code": "MISSING_APP_ID_OR_APP_SECRET"}}), 400

        app_id = request.json.get("app-id")
        app_secret = request.json.get("app-secret")
        app = App.objects.filter(app_id=app_id).first()
        if not app:
            return jsonify({"error": {"code": "INCORRECT_CREDENTIALS"}}), 403

        if bcrypt.hashpw(app_secret, app.app_secret) == app.app_secret:
            # delete the exiting token:
            Access.objects.filter(app=app).delete()
            token = str(uuid.uuid4())
            now = datetime.utcnow().replace(second=0, microsecond=0)
            expires = now + timedelta(days=30)
            Access(app=app, token=token, expires=expires).save()
            expires_3339 = expires.isoformat("T") + "Z"
            return jsonify({"token":token, "expires": expires_3339}), 201

        else:
            return jsonify({"error": {"code": "INCORRECT_CREDENTIALS"}}), 403
