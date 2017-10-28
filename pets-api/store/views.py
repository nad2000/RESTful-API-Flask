from flask.views import MethodView
from flask import Blueprint

from store.api import storeAPI

store_app = Blueprint("store_app", __name__)
store_view=storeAPI.as_view("stores")

store_app.add_url_rule("/stores/", defaults=dict(store_id=None), view_func=store_view,
        methods=["GET", ])
store_app.add_url_rule("/stores/", view_func=store_view, methods=["POST", ])
store_app.add_url_rule(
    "/stores/<int:store_id>",
    view_func=store_view,
    methods=[
        "GET",
        "PUT",
        "DELETE",
    ])
