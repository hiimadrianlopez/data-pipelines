from . import db


class Calendar(db.Model):
    __tablename__ = "calendar"

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.String, nullable=False, unique=True)
    monday = db.Column(db.Integer, nullable=False)
    tuesday = db.Column(db.Integer, nullable=False)
    wednesday = db.Column(db.Integer, nullable=False)
    thursday = db.Column(db.Integer, nullable=False)
    friday = db.Column(db.Integer, nullable=False)
    saturday = db.Column(db.Integer, nullable=False)
    sunday = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String(8), nullable=False)
    end_date = db.Column(db.String(8), nullable=False)

    @property
    def serialize(self):
        return {
            "service_id": self.service_id,
        }

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "detail": f"/services/{self.service_id}/locations",
        }
