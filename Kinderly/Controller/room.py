from Kinderly.Models.room import RoomModel
import Kinderly.Controller.property as pm

class RoomManager:
    schema = RoomModel.schema
    update_schema = RoomModel.schema

    @classmethod
    def get(cls, room_id):
        return RoomModel.fetch(int(room_id))

    @classmethod
    def info(cls, room):
        return {
            "property_id": room.property_id,
            "room_id": room.room_id,
            "capacity": room.capacity,
            "has_attach_bath": room.has_attach_bath,
            "has_ac": room.has_ac,
            "has_heater": room.has_heater,
            "date_added": str(room.dtm_added)
        }

    @classmethod
    def rooms(cls, property):
        rooms = {}
        for i, room in zip(range(len(property.rooms)), property.rooms):
            rooms[i] = RoomManager.info(room)
        return rooms

    @classmethod
    def add(cls, property_id, capacity=1, has_attach_bath=False, has_ac=False, has_heater=False):
        property = pm.PropertyManager.get(property_id)
        property.num_rooms += 1
        room = RoomModel(property_id, capacity, has_attach_bath, has_ac, has_heater)
        room.save()
        return room

    @classmethod
    def owns(cls, user, room_id):
        room = RoomModel.fetch(room_id)
        for p in user.properties:
            if p.property_id == room.property_id:
                return True
        return False

    @classmethod
    def remove(cls, property_id):
        property = pm.PropertyManager.get(property_id)
        property.num_rooms -= 1
        RoomModel.fetch(property_id).delete()

    @classmethod
    def update(cls, room, capacity=None, has_attach_bath=None, has_ac=None, has_heater=None):
        if capacity:
            room.capacity = capacity
        if has_attach_bath:
            room.has_attach_bath = has_attach_bath
        if has_ac:
            room.has_ac = has_ac
        if has_heater:
            room.has_ac = has_heater
        return room.save()
