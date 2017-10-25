from flask.views import MethodView
from flask import jsonify, request, abort

from app.decorators import app_required


class PetAPI(MethodView):

    decorators = [app_required, ]

    pets = [dict(id=pet_id, name=name,
        links=[dict(rel="self", href="/pets/%d" % pet_id), ]) for
        pet_id, name in enumerate(("Mac", "Leo", "Brownie", ), 1)
    ]


    def get(self, pet_id=None):
        if pet_id:
            return jsonify({"pet": self.pets[pet_id-1]}), 200
        return jsonify({"pets": self.pets}), 200

    def post(self):
        if not request.json or not "name" in request.json:
            abort(400)

        pet_id = len(self.pets)+1
        pet = dict(id=pet_id, name=request.json["name"],
            links=[dict(rel="self", href="/pets/%d" % pet_id), ])
        self.pets.append(pet)

        return jsonify(dict(pet=pet)), 201

    def put(self, pet_id=None):  # for "update" you can use PATCH for individual attribute updates
        if not request.json or not "name" in request.json:
            abort(400)
        if pet_id and pet_id < len(self.pets):
            pet = self.pets[pet_id-1]
            pet["name"] = request.json["name"]
            return jsonify({"pet": pet}), 200
        return None, 200

    def patch(self, pet_id=None):  # for "update" you can use PATCH for individual attribute updates
        if not request.json or not "name" in request.json:
            abort(400)
        if pet_id and pet_id < len(self.pets):
            pet = self.pets[pet_id-1]
            pet["name"] = request.json["name"]
            return jsonify({"pet": pet}), 200
        return None, 200

    def delete(self, pet_id=None):
        if pet_id:
            del self.pets[pet_id - 1]
            return jsonify({}), 204
        return jsonify({"pets": self.pets}), 200




