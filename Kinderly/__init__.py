from flask import Flask, jsonify, request, url_for
from flask_restful import Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

app.secret_key = "password"

# SQLAlchemy Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)

# Session Configuration
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # TODO: On production set to True
# PERMANENT_SESSION_LIFETIME  # TODO: Set value on production
app.config["SESSION_TYPE"] = "filesystem"
# SESSION_PERMANENT # TODO: On production set to False
app.config["SESSION_USE_SIGNER"] = True
# app.config["SESSION_SQLALCHEMY"] = db
# app.config["SESSION_SQLALCHEMY_TABLE"] = "Session"


api = Api(app)
session = Session(app)

from Kinderly.Models import user, property, room


@app.before_first_request
def create_databse():
    db.create_all()


@app.route("/test", methods=["GET", "POST"])
def test():
    response = {"response": "success"}
    if request.method == "POST":
        json_data = request.get_json()
        response["message"] = json_data["message"]
    return jsonify(response), 200


from Kinderly.Resources.login import UserLogin

api.add_resource(UserLogin, "/login")

from Kinderly.Resources.register import UserRegister

api.add_resource(UserRegister, "/register")

from Kinderly.Resources.profile import UserProfile

api.add_resource(UserProfile, "/profile")

from Kinderly.Resources.logout import UserLogout

api.add_resource(UserLogout, "/logout")

from Kinderly.Resources.property import Property
api.add_resource(Property, '/property/<int:property_id>', '/property')

from Kinderly.Resources.room import Room
api.add_resource(Room, '/room/<int:room_id>', '/room')

from Kinderly.Resources.property import Properties
api.add_resource(Properties, '/properties')

