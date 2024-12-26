from . import db


class Trip(db.Model):
    __tablename__ = "trip"

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.String, nullable=False)
    trip_id = db.Column(db.String, nullable=False, unique=True)
    trip_headsign = db.Column(db.String)
    trip_short_name = db.Column(db.String)
    direction_id = db.Column(db.Integer, nullable=False)
    block_id = db.Column(db.String)
    shape_id = db.Column(db.Integer, nullable=False)
    wheelchair_accessible = db.Column(db.Integer)
    bikes_allowed = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "route_id": self.route_id,
            "service_id": self.service_id,
            "trip_id": self.trip_id,
            "trip_headsign": self.trip_headsign,
            "trip_short_name": self.trip_short_name,
            "direction_id": self.direction_id,
            "block_id": self.block_id,
            "shape_id": self.shape_id,
            "wheelchair_accessible": self.wheelchair_accessible,
            "bikes_allowed": self.bikes_allowed,
        }
