from flask import request
from flask_restful import Resource
from werkzeug.security import check_password_hash
from jsonschema import validate

from Kinderly.Controller.user import UserManager


class UserLogin(Resource):
    def post(self):
        if UserManager.is_authenticated():
            return {"message": "User is already logged in."}, 400
        else:
            json_data = request.get_json()
            try:
                validate(json_data, UserManager.login_schema)
            except Exception as e:
                print(e)
                return {"message": "Invalid data sent"}, 400

            user = UserManager.get(json_data["mobile"])
            if user:
                if check_password_hash(user.password, json_data["password"].encode("utf-8")):
                    UserManager.set_session(json_data["mobile"])
                    return {"message": "User successfully logged in."}, 200
                else:
                    return {"message": "The username or password entered is incorrect."}, 400
            else:
                return {"message": "The username or password entered is incorrect."}, 400


