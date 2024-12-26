from . import db


class CalendarDate(db.Model):
    __tablename__ = "calendar_date"

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.String(8), nullable=False)
    exception_type = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "service_id": self.service_id,
            "date": self.date,
            "exception_type": self.exception_type,
        }
