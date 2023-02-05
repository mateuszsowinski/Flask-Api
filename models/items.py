from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    price = db.Column(db.Float)
    description = db.Column(db.String(250))
    barcode = db.Column(db.String(12))
    ean = db.Column(db.String(20))
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))

    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates = "items", secondary = "items_tag" )