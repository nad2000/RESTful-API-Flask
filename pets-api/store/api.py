from flask.views import MethodView
from flask import jsonify, request, abort

from app.decorators import app_required


class StoreAPI(MethodView):

    decorators = [app_required, ]

    stores = [dict(id=store_id, name=name,
        links=[dict(rel="self", href="/stores/%d" % store_id), ]) for
        store_id, name in enumerate(("Mac", "Leo", "Brownie", ), 1)
    ]

    def get(self, store_id=None):
        if store_id:
            return jsonify({"store": self.stores[store_id-1]}), 200
        return jsonify({"stores": self.stores}), 200

    def post(self):
        if not request.json or not "name" in request.json:
            abort(400)

        store_id = len(self.stores)+1
        store = dict(id=store_id, name=request.json["name"],
            links=[dict(rel="self", href="/stores/%d" % store_id), ])
        self.stores.append(store)

        return jsonify(dict(store=store)), 201

    def put(self, store_id=None):  # for "update" you can use PATCH for individual attribute updates
        if not request.json or not "name" in request.json:
            abort(400)
        if store_id and store_id < len(self.stores):
            store = self.stores[store_id-1]
            store["name"] = request.json["name"]
            return jsonify({"store": store}), 200
        return None, 200

    def patch(self, store_id=None):  # for "update" you can use PATCH for individual attribute updates
        if not request.json or not "name" in request.json:
            abort(400)
        if store_id and store_id < len(self.stores):
            store = self.stores[store_id-1]
            store["name"] = request.json["name"]
            return jsonify({"store": store}), 200
        return None, 200

    def delete(self, store_id=None):
        if store_id:
            del self.stores[store_id - 1]
            return jsonify({}), 204
        return jsonify({"stores": self.stores}), 200
