from db import db

class TagModel(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))

    store = db.relationship("StoreModel", back_populates = "tags")
    items = db.relationship("ItemModel", back_populates = "tags", secondary = "items_tag" )