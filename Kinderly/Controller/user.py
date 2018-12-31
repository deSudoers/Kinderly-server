from flask import session

import Kinderly.Controller.property as pm
from Kinderly.Models.user import UserModel


class UserManager:

    schema = UserModel.schema
    login_schema = UserModel.login_schema

    @classmethod
    def register(cls, mobile=None, password=None, first_name=None, last_name=None, age=None):
        user = UserModel(mobile, password, first_name, last_name, age)
        user.save()
        return user

    @classmethod
    def get(cls, mobile):
        return UserModel.fetch(mobile)

    @classmethod
    def set_session(cls, mobile):
        session["mobile"] = mobile

    @classmethod
    def is_authenticated(cls):
        if session.get("mobile", None):
            return True
        return False

    @classmethod
    def exists(cls, mobile):
        user = UserModel.fetch(mobile)
        if user:
            return True
        return False

    @classmethod
    def current_user(cls):
        mobile = session.get("mobile", None)
        return UserModel.fetch(mobile)

    @classmethod
    def info(cls, user, show_owned=True):
        info = {
            "user": {
                "mobile": user.mobile,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "image": user.image,
                "favourites": user.favourites
            }
        }
        if show_owned:
            info["properties"] = pm.PropertyManager.owned(user)
        return info


    @classmethod
    def owns(cls, user, property_id):
        for p in user.properties:
            if p.property_id == int(property_id):
                return True
        return False

    @classmethod
    def update_image(cls, image_name):
        user = UserManager.current_user()
        user.image = image_name
        user.save()
