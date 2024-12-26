from . import db


class Shape(db.Model):
    __tablename__ = "shape"

    id = db.Column(db.Integer, primary_key=True)
    shape_id = db.Column(db.Integer, nullable=False)
    shape_pt_lat = db.Column(db.Float, nullable=False)
    shape_pt_lon = db.Column(db.Float, nullable=False)
    shape_pt_sequence = db.Column(db.Integer, nullable=False)
    shape_dist_traveled = db.Column(db.Float)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "shape_id": self.shape_id,
            "shape_pt_lat": self.shape_pt_lat,
            "shape_pt_lon": self.shape_pt_lon,
            "shape_pt_sequence": self.shape_pt_sequence,
            "shape_dist_traveled": self.shape_dist_traveled,
        }
