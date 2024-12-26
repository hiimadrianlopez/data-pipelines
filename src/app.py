from datetime import datetime, timezone
from flask import Flask, jsonify
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from src import config
from src.data import import_data
from src.models import db
from src.routes.services import services_bp
from src.routes.stops import stops_bp
from src.routes.town_halls import town_halls_bp

app = Flask(__name__)
app.config.from_object("src.config")

db.init_app(app)
migrate = Migrate(app, db)


@app.errorhandler(HTTPException)
def handle_http_error(error):
    return (
        jsonify(
            {
                "message": error.description,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ),
        error.code,
    )


@app.after_request
def add_timestamp(response):
    if response.content_type == "application/json":
        response_data = response.get_json()
        if response_data is not None:
            response_data["timestamp"] = datetime.now(timezone.utc).isoformat()
            response.set_data(jsonify(response_data).data)
    return response


@app.route("/health-check")
def health_check():
    return (
        jsonify({"message": "healthy"}),
        200,
    )


app.register_blueprint(stops_bp, url_prefix="/stops")
app.register_blueprint(services_bp, url_prefix="/services")
app.register_blueprint(town_halls_bp, url_prefix="/town-halls")


if __name__ == "__main__":
    import_data()
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT)
