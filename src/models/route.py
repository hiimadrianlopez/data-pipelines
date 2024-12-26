from . import db


class Route(db.Model):
    __tablename__ = "route"

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, nullable=False, unique=True)
    agency_id = db.Column(db.Integer, nullable=False)
    route_short_name = db.Column(db.String)
    route_long_name = db.Column(db.String)
    route_desc = db.Column(db.String)
    route_type = db.Column(db.Integer, nullable=False)
    route_url = db.Column(db.String)
    route_color = db.Column(db.String)
    route_text_color = db.Column(db.String)
    route_sort_order = db.Column(db.Integer)
    continuous_pickup = db.Column(db.String)
    continuous_drop_off = db.Column(db.String)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "route_id": self.route_id,
            "agency_id": self.agency_id,
            "route_short_name": self.route_short_name,
            "route_long_name": self.route_long_name,
            "route_desc": self.route_desc,
            "route_type": self.route_type,
            "route_url": self.route_url,
            "route_color": self.route_color,
            "route_text_color": self.route_text_color,
            "route_sort_order": self.route_sort_order,
            "continuous_pickup": self.continuous_pickup,
            "continuous_drop_off": self.continuous_drop_off,
        }
