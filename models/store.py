from db import db

class StoreModel(db.Model):
    __tablename__ = "store"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(90), unique = True)
    items = db.relationship("ItemModel", back_populates="store", lazy = "dynamic")
    tags = db.relationship("TagModel", back_populates = "store", lazy = "dynamic")