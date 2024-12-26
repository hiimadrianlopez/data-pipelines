from . import db


class Agency(db.Model):
    __tablename__ = "agency"

    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, unique=True)
    agency_name = db.Column(db.String)
    agency_url = db.Column(db.String)
    agency_timezone = db.Column(db.String)
    agency_lang = db.Column(db.String)
    agency_phone = db.Column(db.String)
    agency_fare_url = db.Column(db.String)
    agency_email = db.Column(db.String)

    @property
    def serialize(self):
        return {
            "id": self.agency_id,
            "name": self.agency_name,
            "url": self.agency_url,
            "timezone": self.agency_timezone,
            "lang": self.agency_lang,
            "phone": self.agency_phone,
            "fare_url": self.agency_fare_url,
            "email": self.agency_email,
        }
