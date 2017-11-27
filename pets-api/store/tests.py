from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
import json
from datetime import datetime, timedelta


from settings import MONGODB_HOST, MONGODB_DB
from store.models import Store
from application import fixtures


class StoreTest(unittest.TestCase):

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

    def store_dict(self):
        return json.dumps(dict(
            neighborhood="Broxville",
            street_address="1112 Bronxville Avenue",
            city="Bronx",
            state="NY",
            zip="10567",
            phone="718-222-2445",
        ))


    def create_api_app(self):
        app_dict = self.app_dict()
        rv = self.app.post(
                "/apps/",
                data=app_dict,
                content_type="application/json")
        return rv

    def get_access_token(self):
        app_dict = self.app_dict()
        rv = self.app.post(
            "/apps/access_token/",
            data=app_dict,
            content_type="application/json")

        rv = self.app.post(
            "/apps/access_token/", data=app_dict, content_type="application/json")
        self.token = json.loads(rv.data.decode("utf-8")).get("token")


    def headers(self):
        return {
            "X-APP-ID": "pet_client",
            "X-APP-TOKEN": self.token,
        }

    def test_stores(self):
        self.create_api_app()
        self.get_access_token()

        # create a store
        rv = self.app.post(
                "/stores/",
                headers=self.headers(),
                data=self.store_dict(),
                content_type="application/json")
        assert rv.status_code == 201
        store_id = json.loads(rv.data.decode("utf-8")).get("store")["id"]

        # get a store:
        rv = self.app.get(
                "/stores/" + store_id,
                headers=self.headers(),
                data=self.app_dict(),
                content_type="application/json")
        assert rv.status_code == 200
        store = json.loads(rv.data.decode("utf-8")).get("store")

        # edit a store:
        new_store = json.dumps(dict(
            neighborhood="Dyker Heights",
            street_address="55 16th Avenue",
            city="Brooklyn",
            state="NY",
            zip="11215",
            phone="718-555-5555",
        ))

        rv = self.app.put(
                "/stores/" + store_id,
                headers=self.headers(),
                data=new_store,
                content_type="application/json")

        assert rv.status_code == 200
        store = json.loads(rv.data.decode("utf-8")).get("store")
        assert store["phone"] == "718-555-5555"

        # delete store
        rv = self.app.delete(
                "/stores/" + store_id,
                headers=self.headers(),
                content_type="application/json")
        assert rv.status_code == 204
        assert Store.objects.filter(live=False).count() == 1

    def test_spagination(self):
        self.create_api_app()
        self.get_access_token()

        fixtures(self.db_name, "store", "store/fixtures/stores.json")

        # create a store
        rv = self.app.get(
                "/stores/",
                headers=self.headers(),
                content_type="application/json")
        assert rv.status_code == 200
        assert "next" in str(rv.data)

        # get second page of stores
        rv = self.app.get(
                "/stores/?page=2",
                headers=self.headers(),
                content_type="application/json")
        assert rv.status_code == 200
        assert "next" in str(rv.data)
        assert "previous" in str(rv.data)
