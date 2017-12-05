from application import db
from store.models import Store


class Pet(db.Document):
    external_id = db.StringField(db_field="ei")
    name = db.StringField(db_field="n")
    species = db.StringField(db_field="s")
    breed = db.StringField(db_field="b")
    age = db.IntField(db_field="a")
    store = db.ReferenceField(Store, db_field="st")
    price = db.DecimalField(
        db_field="p", precision=2, rounding="ROUND_HALF_UP")
    sold = db.BooleanField(db_field="sl", default=False)
    received_date = db.DateTimeField(db_field="rd")
    sold_date = db.DateTimeField(db_field="sd")
    live = db.BooleanField(db_field="l", default=True)

    meta = {
        "indexes": [("external_id", "live"), ("species", "breed", "live"),
                    ("store", "live")]
    }

    @property
    def links(self):
        return dict(rel="self", href="/pets/" + self.external_id)

    def to_obj(self):
        obj = {
            "id" if f == "external_id" else f:  self.store.to_obj()
            if f == "store" else str(self[f]) if f == "price" else self[f]
            for f in self._fields if f not in (
                "_id",
                "id",
            )
        }
        obj["links"] = self.links
        return obj
