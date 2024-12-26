import geopandas as gpd
from flask import abort
from shapely.geometry import Point

from . import db
from .. import config


class Stop(db.Model):
    __tablename__ = "stop"

    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.String, nullable=False)
    stop_code = db.Column(db.String)
    stop_name = db.Column(db.String, nullable=False)
    stop_desc = db.Column(db.String)
    stop_lat = db.Column(db.Float, nullable=False)
    stop_lon = db.Column(db.Float, nullable=False)
    zone_id = db.Column(db.String)
    stop_url = db.Column(db.String)
    location_type = db.Column(db.Integer)
    parent_station = db.Column(db.String)
    stop_timezone = db.Column(db.String)
    wheelchair_boarding = db.Column(db.Integer)
    level_id = db.Column(db.String)
    platform_code = db.Column(db.String)

    @property
    def serialize(self):
        return {
            "id": self.stop_id,
            "name": self.stop_name,
            "lat": self.stop_lat,
            "lon": self.stop_lon,
            "detail": f"/stops/{self.stop_id}",
            "town_hall": self.get_town_hall(),
        }

    def to_dict(self):
        return {
            "id": self.stop_id,
            "name": self.stop_name,
            "lat": self.stop_lat,
            "lon": self.stop_lon,
            "town_hall": self.get_town_hall(),
        }

    def get_town_hall(self):
        try:
            gdf = gpd.read_file(config.POLIGONS_GEOJSON_PATH)
            point = Point(self.stop_lon, self.stop_lat)
            result = gdf[gdf.contains(point)]

            if result.empty:
                abort(404, description="No town hall found for the given coordinates.")

            return result["NOMGEO"].values[0]
        except Exception as e:
            abort(500, description=f"Error while determining the town hall: {str(e)}")
