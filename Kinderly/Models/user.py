import datetime

from Kinderly import db


class UserModel(db.Model):

    __tablename__ = "User"

    user_id = db.Column("UserID", db.Integer, primary_key=True)
    mobile = db.Column("Mobile", db.Integer)
    password = db.Column("Password", db.String(300))
    first_name = db.Column("FirstName", db.String(80))
    last_name = db.Column("LastName", db.String(80))
    age = db.Column("Age", db.Integer)
    properties = db.relationship("PropertyModel", cascade="all,delete,delete-orphan")
    image = db.Column("Image", db.String)
    dtm_added = db.Column("DtmAdded", db.DateTime, default=datetime.datetime.utcnow())

    schema = {
        "type": "object",
        "properties": {
            "mobile": {"type": "number"},
            "password": {"type": "string"},
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "age": {"type": "number"},
        },
        "required": ["mobile", "password", "first_name", "last_name", "age"]
    }

    login_schema = {
        "type": "object",
        "properties": {
            "mobile": {"type": "number"},
            "password": {"type": "string"}
        },
        "required": ["mobile", "password"]
    }

    def __init__(self, mobile=None, password=None, first_name=None, last_name=None, age=None, image=""):
        self.mobile = mobile
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.image = image
        self.dtm_dded = datetime.datetime.utcnow()

    @classmethod
    def fetch(cls, mobile):
        return cls.query.filter_by(mobile=mobile).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
