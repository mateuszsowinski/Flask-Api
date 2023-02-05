from models.users import UserModel
from flask_smorest import abort, Blueprint, response
from flask.views import MethodView
from schemas import UserSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blocklist import BLOCKED

blp = Blueprint("Users", __name__, description = "Users in API")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        bytes = user_data["password"].encode('utf-8')
        salt = bcrypt.gensalt()
        user = UserModel()
        user.login = user_data["login"]
        user.password = bcrypt.hashpw(bytes,salt)
        db.session.add(user)
        db.session.commit()
        return {"message" : "User create"}, 201

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message" : "Delete user"}, 200

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.login == user_data["login"]).first()
        userBytes = user_data["password"].encode('utf-8')
        password = bcrypt.checkpw(userBytes, user.password)
        if user and password:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token" : refresh_token}
        abort(401, message = "Invalid credentials")

@blp.route("/logout")
class UserLogout(MethodView):
    @blp.response(200)
    @jwt_required()
    def post(self):
        jwt = get_jwt()["jti"]
        BLOCKED.add(jwt)
        return {"message" : "Succes logout"}

@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_identiy = get_jwt_identity()
        new_token = create_access_token(user_identiy, fresh=False)
        return {"access_token": new_token}