from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from jsonschema import validate

from Kinderly.Controller.user import UserManager


class UserRegister(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            validate(json_data, UserManager.schema)
        except Exception as e:
            print(e)
            return {"message": "Invalid data sent"}, 400

        if not UserManager.exists(json_data["mobile"]):
            try:
                hashed_pw = generate_password_hash(json_data["password"].encode("utf-8"))
                user = UserManager.register(json_data["mobile"], hashed_pw, json_data["first_name"], json_data["last_name"], json_data["age"])
            except Exception as e:
                print(e)
                return {"message": "An error occurred while registering."}, 500

            UserManager.set_session(user.mobile)

            return {"message": "User successfully registered."}, 200
        else:
            return {"message": "A user with the same mobile number already exists."}, 400

