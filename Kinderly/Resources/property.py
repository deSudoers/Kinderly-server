from flask import request
from flask_restful import Resource
from jsonschema import validate
import json

from Kinderly.Controller.property import PropertyManager
from Kinderly.Controller.user import UserManager


class Property(Resource):
    def get(self, property_id):
        if UserManager.is_authenticated():
            property = PropertyManager.get(property_id)
            if property:
                return PropertyManager.info(property)
            else:
                return {"message": "Could ntro"
                                   "t find property"}, 400
        return {"message": "User not logged in."}, 401

    def put(self, property_id):
        if UserManager.is_authenticated():
            json_data = request.get_json()
            try:
                validate(json_data, PropertyManager.update_schema)
            except Exception as e:
                print(e)
                return {"message": "Invalid data sent"}, 400
            if PropertyManager.owns(UserManager.current_user(), property_id):
                property = PropertyManager.get(property_id)
                PropertyManager.update(property, json_data.get("address, None"), json_data.get("price, None"), json_data.get("type, None"), json_data.get("extras, None"))
                return {"message": "Property updated"}, 200
            else:
                return {"message": "Could not find property"}, 400
        return {"message": "User not logged in."}, 401

    def delete(self, property_id):
        if UserManager.is_authenticated():
            if PropertyManager.owns(UserManager.current_user(), property_id):
                try:
                    PropertyManager.remove(property_id)
                except Exception as e:
                    print(e)
                    return {"message": "An error occurred while deleting"}, 500
                return {"message": "Property removed"}, 200
            else:
                return {"message": "Could not find property"}, 400
        return {"message": "User not logged in."}, 401

    def post(self):
        if UserManager.is_authenticated():
            user = UserManager.current_user()
            json_data = request.get_json()
            try:
                validate(json_data, PropertyManager.schema)
            except Exception as e:
                print(e)
                return {"message": "Invalid data sent"}, 400
            property = PropertyManager.add(user.user_id, json_data["address"], json_data["price"], json_data["type"], json_data.get("extras", None))
            return {"property_id": property.property_id}, 200


class PropertyImage:
    def post(self):
        pass

class Properties(Resource):
    def post(self):
        if UserManager.is_authenticated():
            json_data = request.get_json()
            try:
                validate(json_data, PropertyManager.filter_schema)
            except Exception as e:
                print(e)
                return {"message": "Invalid data sent"}, 400

            return PropertyManager.filter(address=json_data.get("address", None), min_price=json_data.get("min_price", None), max_price=json_data.get("max_price", None), num_rooms=json_data.get("num_rooms", None),
                                          capacity=json_data.get("capacity", None)), 200
        return {"message": "User not logged in."}, 401


