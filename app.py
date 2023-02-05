from flask import Flask, jsonify
from db import db
from blocklist import BLOCKED
import models
import secrets
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from resources.store import blp as StoreBlueprint
from resources.items import blp as ItemsBlueprint
from resources.tags import blp as TagsBlueprint
from resources.user import blp as UserBlueprint



def create_app(db_url = None):
    app = Flask(__name__)
    load_dotenv()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores API"
    app.config["API_VERSION"] = "0.1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)
    # secrets.SystemRandom().getrandbits(256)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    @jwt.token_in_blocklist_loader
    def check_token_in_blockedlist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKED


    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(TagsBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

        
