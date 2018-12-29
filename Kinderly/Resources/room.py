from flask import request
from flask_restful import Resource
from jsonschema import validate

from Kinderly.Controller.room import RoomManager
from Kinderly.Controller.user import UserManager


class Room(Resource):
    def delete(self, room_id):
        if UserManager.is_authenticated():
            if RoomManager.owns(UserManager.current_user(), room_id):
                try:
                    RoomManager.remove(room_id)
                except Exception as e:
                    print(e)
                    return {"message": "An error occurred while deleting"}, 500
                return {"message": "Room removed"}, 200
            else:
                return {"message": "Could not find room"}, 400
        return {"message": "User not logged in."}, 401

    def put(self, room_id):
        if UserManager.is_authenticated():
            json_data = request.get_json()
            try:
                validate(json_data, RoomManager.update_schema)
            except Exception as e:
                print(e)
                return {"message": "Invalid data sent"}, 400
            if RoomManager.owns(UserManager.current_user(), room_id):
                room = RoomManager.get(room_id)
                RoomManager.update(room, json_data.get("capacity", None), json_data.get("has_attach_bath", None), json_data.get("has_ac", None), json_data.get("has_heater", None))
                return {"message": "Room updated"}, 200
            else:
                return {"message": "Could not find room"}, 400
        return {"message": "User not logged in."}, 401

    def post(self):
        if UserManager.is_authenticated():
            json_data = request.get_json()
            try:
                validate(json_data, RoomManager.schema)
            except Exception as e:
                print(e)
                return {"message": "Invalid data sent"}, 400

            if UserManager.owns(UserManager.current_user(), json_data["property_id"]):
                room = RoomManager.add(json_data["property_id"], json_data.get("capacity", None), json_data.get("has_attach_bath", None), json_data.get("has_ac", None), json_data.get("has_heater", None))
                return {"room_id": room.room_id}
            else:
                return {"message": "User doesn't have permission to add room to given property"}, 400
        return {"message": "User not logged in."}, 401
