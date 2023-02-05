from db import db

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(250), nullable = False)