import datetime
from Kinderly import db


class RoomModel(db.Model):

    __tablename__ = "Room"

    room_id = db.Column("RoomID", db.Integer, primary_key=True)
    capacity = db.Column("Capacity", db.Integer)
    has_attach_bath = db.Column("HasAttachBath", db.Boolean)
    has_ac = db.Column("HasAC", db.Boolean)
    has_heater = db.Column("HasHeater", db.Boolean)
    property_id = db.Column(db.Integer, db.ForeignKey('Property.PropertyID'))
    property = db.relationship("PropertyModel", back_populates="rooms")
    dtm_added = db.Column("DtmAdded", db.DateTime, default=datetime.datetime.utcnow())

    schema = {
        "type": "object",
        "properties": {
            "property_id": {"type": "number"},
            "capacity": {"type": "number"},
            "has_attach_bath": {"type": "boolean"},
            "has_ac": {"type": "boolean"},
            "has_heater": {"type": "boolean"}
        },
        "required": ["property_id"]
    }

    update_schema = {
        "type": "object",
        "properties": {
            "capacity": {"type": "number"},
            "has_attach_bath": {"type": "boolean"},
            "has_ac": {"type": "boolean"},
            "has_heater": {"type": "boolean"}
        }
    }

    def __init__(self, property_id, capacity=1, has_attach_bath=False, has_ac=False, has_heater=False):
        self.property_id = property_id
        self.capacity = capacity
        self.has_attach_bath = has_attach_bath
        self.has_ac = has_ac
        self.has_heater = has_heater
        self.dtm_added = datetime.datetime.utcnow()

    @classmethod
    def fetch(cls, room_id):
        return cls.query.filter_by(room_id=room_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
