from mongoengine import signals
from application import db

class Store(db.Document):
    external_id = db.StringField(db_field="ei")
    neignborhood = db.StringField(db_field="n")
    street_address = db.StringField(db_field="sa")
    city = db.StringField(db_field="c")
    state = db.StringField(db_field="st")
    zip = db.StringField(db_field="z")
    phone = db.StringField(db_field="p")

    meta = dict(indexes=[("external_id", )])

    @property
    def links(self):
        return dict(rel="self", href="/stores/" + self.external_id)

    def to_obj(self):
        obj = {f: self[f] for f in self._fields}
        obj["links"] = self.links
        return obj

