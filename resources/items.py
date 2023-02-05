from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from models.items import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
 
blp = Blueprint("Items", __name__, description = "Items")

@blp.route("/item")
class Item(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)  
    def post(self,item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message= "Failed") 
        return item

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)
    def get(self, item_id):
        
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message" : "Deleted succesfully"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data ,item_id):
        
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(**item_data)

        db.session.add(item)
        db.session.commit()

        return item
