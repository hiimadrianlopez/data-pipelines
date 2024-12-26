import uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

from . import db


class TownHall(db.Model):
    __tablename__ = "town_hall"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    name = db.Column(db.String)
    slug = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    meta_data = db.Column(JSONB)

    @property
    def serialize(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "slug": self.slug,
            "stops": f"/town-halls/stops/{self.slug}",
        }
