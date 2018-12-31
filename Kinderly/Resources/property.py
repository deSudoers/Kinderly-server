from flask import request
from flask_restful import Resource
from jsonschema import validate
from PIL import Image
import json, os

from Kinderly.Controller.property import PropertyManager
from Kinderly.Controller.user import UserManager

UPLOAD_FOLDER = 'Kinderly/static/images'


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


class PropertyImage(Resource):
    def post(self, property_id):
        if UserManager.is_authenticated():
            photo = request.files['image']
            if photo:
                dir = os.path.join(UPLOAD_FOLDER + "/" + str(property_id))
                if not os.path.isdir(dir):
                    os.mkdir(dir)
                num = len(os.listdir(dir))
                filename = str(num) + ".jpg"
                photo = Image.open(photo)
                photo.save(os.path.join(UPLOAD_FOLDER, str(property_id), filename), quality=20, optimize=True)
                property = PropertyManager.get(property_id)
                p_images = property.images.split()
                p_images.append(filename)
                property.images = " ".join(p_images)
                property.save()
                return {"message": "Profile picture saved"}, 200
            else:
                return {'message':'No file found'}, 500
        return {"message": "User not logged in."}, 401


class Properties(Resource):
    def post(self):
        if UserManager.is_authenticated():
            json_data = request.get_json()
            try:
                validate(json_data, PropertyManager.filter_schema)
            except Exception as e:
                print(e)
                return {"message": "Invalid data sent"}, 400

            return PropertyManager.filter(address=json_data.get("address", ""), min_price=json_data.get("min_price", "0.0"), max_price=json_data.get("max_price", "100000.0"), num_rooms=json_data.get("num_rooms", None),
                                          capacity=json_data.get("capacity", None), has_attach_bath=json_data.get("attach_bath", None)), 200
        return {"message": "User not logged in."}, 40

class PropertyFavourites(Resource):
    def post(self):
        if UserManager.is_authenticated():
            json_data = request.get_json()
            if json_data["property_id"] and json_data["favourite"] is not None:
                if json_data["favourite"]:
                    if PropertyManager.exists(int(json_data["property_id"])):
                        user = UserManager.current_user()
                        favs = user.favourites.split()
                        if json_data["property_id"] not in favs:
                            favs.append(json_data["property_id"])
                            user.favourites = " ".join(favs)
                            user.save()
                        return {"message": "Saved"}, 200
                    return {"message": "Property doesn't exist"}, 400
                else:
                    user = UserManager.current_user()
                    favs = user.favourites.split()
                    if (json_data["property_id"]) in favs: favs.remove(json_data["property_id"])
                    user.favourites = " ".join(favs)
                    user.save()
                    return {"message": "Deleted"}, 200
            else:
                return {"message": "Invalid data sent"}, 400
        return {"message": "User not logged in."}, 401

    def get(self):
        if UserManager.is_authenticated():
            user = UserManager.current_user()
            favs = user.favourites.split()
            properties = {}
            i = 0
            for p in favs:
                if PropertyManager.exists(int(p)):
                    properties[i] = PropertyManager.info(PropertyManager.get(int(p)))
                    i += 1
            return properties, 200

        return {"message": "User not logged in."}, 401

