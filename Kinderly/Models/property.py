import datetime

from Kinderly import db


class PropertyModel(db.Model):

    __tablename__ = "Property"

    property_id = db.Column("PropertyID", db.Integer, primary_key=True)
    address = db.Column("Address", db.String(300))
    location = db.Column("Location", db.String)
    price = db.Column("Price", db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('User.UserID'))
    user = db.relationship("UserModel", back_populates="properties")
    type = db.Column("Type", db.String(20))
    num_rooms = db.Column("NumRooms", db.Integer)
    extras = db.Column("Extras", db.String)
    rooms = db.relationship("RoomModel", cascade="all,delete,delete-orphan")
    dtm_added = db.Column("DtmAdded", db.DateTime, default=datetime.datetime.utcnow())

    schema = {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
            "price": {"type": "number"},
            "type": {"type": "string"},
            "extras": {"type": "string"}
        },
        "required": ["address", "price", "type"]
    }

    update_schema = {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
            "price": {"type": "number"},
            "type": {"type": "string"},
            "extras": {"type": "string"}
        }
    }

    filter_schema = {
        "type": "object",
        "properties": {
            "address": {"type": "string"},
            "min_price": {"type": "number"},
            "max_price": {"type": "number"},
            "num_rooms": {"type": "number"},
            "capacity": {"type": "number"},
            "attach_bath": {"type": "boolean"}
        }
    }

    def __init__(self, user_id, address=None, price=0.0, type=None, extras=None, location="0, 0"):
        self.user_id = user_id
        self.address = address
        self.price = price
        self.type = type
        self.extras = extras
        self.num_rooms = 0
        self.location = location
        self.dtm_dded = datetime.datetime.utcnow()

    @classmethod
    def fetch(cls, property_id):
        return cls.query.filter_by(property_id=property_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
