from models.items import ItemModel
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from schemas import TagItemSchema, TagSchema
from models import TagModel, StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
 
blp = Blueprint("Tags", __name__, description = "Tagi do sklepów")

@blp.route("/tag")
class Tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        return tags

@blp.route("/tag/<int:tag_id>")
class Tags(MethodView):
    @blp.response(202, description= 'Delete tag', example={"message" :"Tag deleted..." })
    @blp.alt_response(404, description= "Tag not found")
    @blp.alt_response(400, description= "znaleziono więcej...")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "delete"}
        abort(400, message = "Sprawdź czy tag nie jest przypisany do jakiegoś przedmiotu")


@blp.route("/item/<int:store_id>/tags")
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        tags = store.tags.all()
        return tags

    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)  
    def post(self,tag_data, store_id):
        tag = TagModel(**tag_data, store_id = store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message= "Failed") 
        return tag

@blp.route("/item/<int:store_id>/tags/<int:tag_id>")
class TagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post (self, store_id, tag_id):
        item = ItemModel.query.get_or_404(store_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "coś poszło nie tak")
        return tag
 
    @blp.response(201, TagItemSchema)
    def delete (self, store_id, tag_id):
        item = ItemModel.query.get_or_404(store_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "coś poszło nie tak")
        return {"message" : "Usunięto tag z przedmiotu", "items" : item, "tags": tag}
