from models.store import StoreModel
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import StoreSchema
from db import db

blp = Blueprint("Store", __name__, description = "wcwc")



@blp.route("/store")
class Store(MethodView):
    @blp.response(200,StoreSchema(many = True))
    def get(self):
        store = StoreModel.query.all()
        return store


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message" : "Deleted succesfully"}
        
