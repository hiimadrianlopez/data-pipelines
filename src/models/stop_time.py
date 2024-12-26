from . import db


class StopTime(db.Model):
    __tablename__ = "stop_time"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.String, nullable=False)
    arrival_time = db.Column(db.String, nullable=False)
    departure_time = db.Column(db.String, nullable=False)
    stop_id = db.Column(db.String, nullable=False)
    stop_sequence = db.Column(db.Integer, nullable=False)
    stop_headsign = db.Column(db.String)
    pickup_type = db.Column(db.Integer)
    drop_off_type = db.Column(db.Integer)
    continuous_pickup = db.Column(db.String)
    continuous_drop_off = db.Column(db.String)
    shape_dist_traveled = db.Column(db.Float)
    timepoint = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "arrival_time": self.arrival_time,
            "departure_time": self.departure_time,
            "stop_id": self.stop_id,
            "stop_sequence": self.stop_sequence,
            "stop_headsign": self.stop_headsign,
            "pickup_type": self.pickup_type,
            "drop_off_type": self.drop_off_type,
            "continuous_pickup": self.continuous_pickup,
            "continuous_drop_off": self.continuous_drop_off,
            "shape_dist_traveled": self.shape_dist_traveled,
            "timepoint": self.timepoint,
        }
