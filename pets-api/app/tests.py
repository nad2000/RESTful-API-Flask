from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
import json
from datetime import datetime, timedelta


from app.models import App, Access
from settings import MONGODB_HOST


class AppTest(unittest.TestCase):

    def create_app(self):
        self.db_name = "pets-api-test"
        return create_app_base(
            MONGODB_SETTINGS={"DB": self.db_name,
                              "HOST": MONGODB_HOST},
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY="aHJ#JK@H$H@#$#$J",
        )

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)

    def app_dict(self):
        return json.dumps({
            "app-id": "pet_client",
            "app-secret": "pet_service",
        })

    def test_create_app_basic_registration(self):
        rv = self.app.post(
            "/apps/", data=self.app_dict(), content_type="application/json")
        assert rv.status_code == 201

        # reissue:
        rv = self.app.post(
            "/apps/", data=self.app_dict(), content_type="application/json")
        assert "APP_ID_ALREADY_EXISTS" in str(rv.data)

    def test_create_app_missing_app_secret(self):
        app_dict = json.dumps({"app-id": "pet_client"})
        rv = self.app.post(
            "/apps/", data=app_dict, content_type="application/json")
        assert "MISSING_APP_ID_OR_APP_SECRET" in str(rv.data)

    def test_token_generation(self):
        app_dict = self.app_dict()
        rv = self.app.post(
            "/apps/", data=app_dict, content_type="application/json")
        assert rv.status_code == 201

        rv = self.app.post(
            "/apps/access_token/", data=app_dict, content_type="application/json")
        assert rv.status_code == 201
        token = json.loads(rv.data.decode("utf-8")).get("token")
        assert token is not None or token != ''

        incorrect_app_dict = json.dumps({
            "app-id": "pet_client",
            "app-secret": "BAD SECRET!",
        })
        rv = self.app.post(
            "/apps/access_token/", data=incorrect_app_dict, content_type="application/json")
        print(rv.status_code)
        assert rv.status_code == 403
        assert "INCORRECT_CREDENTIALS" in str(rv.data)

        incorrect_app_dict = json.dumps({
            "app-id": "pet_client",
        })
        rv = self.app.post(
            "/apps/access_token/",
            data=incorrect_app_dict,
            content_type="application/json")
        assert rv.status_code == 400
        assert "MISSING_APP_ID_OR_APP_SECRET" in str(rv.data)

        # test exprired token
        now = datetime.utcnow().replace(second=0, microsecond=0)
        expires = now + timedelta(days=-31)
        access = Access.objects.first()
        access.expires = expires
        access.save()

        rv = self.app.get("/pets/",
                headers={
                    "X-APP-ID": "pet_client",
                    "X-APP-TOKEN": token},
                content_type="application/json")
        assert "TOKEN_EXPIRED" in str(rv.data)
