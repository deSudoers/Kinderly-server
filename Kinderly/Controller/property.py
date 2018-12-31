import sqlalchemy
import requests
from sqlalchemy.sql.expression import true, false

from Kinderly.Models.property import PropertyModel
from Kinderly.Models.room import RoomModel
import Kinderly.Controller.room as rm
import Kinderly.Controller.user as um


class PropertyManager:
    schema = PropertyModel.schema
    update_schema = PropertyModel.update_schema
    filter_schema = PropertyModel.filter_schema

    @classmethod
    def get(cls, property_id):
        return PropertyModel.fetch(int(property_id))

    @classmethod
    def add(cls, user_id, address=None, price=0.0, type=None, extras=None):
        location = PropertyManager.location(address)
        property = PropertyModel(user_id, address, price, type, extras, location)
        property.save()
        return property


    @classmethod
    def info(cls, property):
        user = property.user

        return {
            "property_id": property.property_id,
            "address": property.address,
            "price": property.price,
            "location": property.location,
            "type": property.type,
            "extras": property.extras,
            "rooms": rm.RoomManager.rooms(property),
            "num_rooms": property.num_rooms,
            "user": um.UserManager.info(user, show_owned=False)["user"],
            "date_added": str(property.dtm_added),
            "images": {k: v for k, v in enumerate(property.images.split())}
        }

    @classmethod
    def owned(cls, user):
        properties = {}
        for i, property in zip(range(len(user.properties)), user.properties):
            properties[i] = {
                "property_id": property.property_id,
                "address": property.address,
                "price": property.price,
                "location": property.location,
                "type": property.type,
                "extras": property.extras,
                "rooms": rm.RoomManager.rooms(property),
                "num_rooms": property.num_rooms,
                "date_added": str(property.dtm_added)
            }
        return properties

    @classmethod
    def exists(cls, property_id):
        property = PropertyModel.fetch(property_id)
        if property:
            return True
        return False

    @classmethod
    def update(cls, property, address=None, price=None, type=None, extras=None):
        if address:
            property.address = address
            property.location = PropertyManager.location(address)
        if price:
            property.price = price
        if type:
            property.type = type
        if extras:
            property.extras = extras
        return property.save()

    @classmethod
    def owns(cls, user, property_id):
        for p in user.properties:
            if p.property_id == property_id:
                return True
        return False

    @classmethod
    def remove(cls, property_id):
        PropertyModel.fetch(property_id).delete()

    @classmethod
    def filter(cls, address="", min_price=0.0, max_price=100000, num_rooms=None, capacity=None, has_attach_bath=None):
        queries = [PropertyModel.address.like("%" + address + "%"), PropertyModel.price.between(min_price, max_price)]

        if num_rooms:
            queries.append(PropertyModel.num_rooms == num_rooms)

        if capacity:
            queries.append(RoomModel.capacity == capacity)

        if has_attach_bath:
            queries.append(RoomModel.has_attach_bath.is_(has_attach_bath))

        property_list = PropertyModel.query.join(RoomModel).filter(sqlalchemy.and_(*queries)).all()

        properties = {}

        for i, property in zip(range(len(property_list)), property_list):
            properties[i] = {
                "property_id": property.property_id,
                "address": property.address,
                "price": property.price,
                "type": property.type,
                "num_rooms": property.num_rooms,
                "images": {k: v for k, v in enumerate(property.images.split())}
            }

        user = um.UserManager.current_user()
        favs = user.favourites.split()
        fav_properties = {}
        i = 0
        for p in favs:
            if PropertyManager.exists(int(p)):
                fav_properties[i] = int(p)
                i += 1

        properties["favourites"] = fav_properties

        return properties

    @classmethod
    def location(cls, address):
        payload = {'key': 'AIzaSyDGo-6VLrdkGeSQ-YxpxyIKuXW3zegKQ1Y', 'address': address}
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload)
        json = r.json()
        if json["status"] == "OK":
            location = json["results"][0]["geometry"]["location"]
            return str(location["lat"]) + ", " + str(location["lng"])
        return "0, 0"
