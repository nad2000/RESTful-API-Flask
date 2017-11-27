from mongoengine import signals
from application import db

class Store(db.Document):
    external_id = db.StringField(db_field="ei")
    neighborhood = db.StringField(db_field="n")
    street_address = db.StringField(db_field="sa")
    city = db.StringField(db_field="c")
    state = db.StringField(db_field="st")
    zip = db.StringField(db_field="z")
    phone = db.StringField(db_field="p")
    live = db.BooleanField(db_field="l", default=True)

    meta = dict(indexes=[("external_id", "live", )])

    @property
    def links(self):
        return dict(rel="self", href="/stores/" + self.external_id)

    def to_obj(self):
        obj = {"id" if f == "external_id" else f: self[f] for f in self._fields if f not in ("_id", "id", )}
        obj["links"] = self.links
        return obj

