from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    barcode = db.Column(db.String)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))

    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates = "items", secondary = "items_tag" )