from . import db


class FeedInfo(db.Model):
    __tablename__ = "feed_info"

    id = db.Column(db.Integer, primary_key=True)
    feed_publisher_name = db.Column(db.String, nullable=False)
    feed_publisher_url = db.Column(db.String, nullable=False)
    feed_lang = db.Column(db.String, nullable=False)
    default_lang = db.Column(db.String)
    feed_start_date = db.Column(db.String(8), nullable=False)
    feed_end_date = db.Column(db.String(8), nullable=False)
    feed_version = db.Column(db.Integer, nullable=False)
    feed_contact_email = db.Column(db.String)
    feed_contact_url = db.Column(db.String, nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "feed_publisher_name": self.feed_publisher_name,
            "feed_publisher_url": self.feed_publisher_url,
            "feed_lang": self.feed_lang,
            "default_lang": self.default_lang,
            "feed_start_date": self.feed_start_date,
            "feed_end_date": self.feed_end_date,
            "feed_version": self.feed_version,
            "feed_contact_email": self.feed_contact_email,
            "feed_contact_url": self.feed_contact_url,
        }
