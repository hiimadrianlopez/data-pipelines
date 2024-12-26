import geopandas as gpd
from flask import Blueprint, abort, jsonify, request
from shapely.geometry import Point

from src import config
from src.models.stop import Stop
from src.models.town_hall import TownHall

town_halls_bp = Blueprint("town-halls", __name__)


@town_halls_bp.route("/", methods=["GET"])
def get_all():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated = TownHall.query.paginate(page=page, per_page=per_page, error_out=False)
    serialized = [stop.serialize for stop in paginated.items]
    if not serialized:
        abort(404, "Items not found!")

    response = {
        "data": serialized,
        "pagination": {
            "total_items": paginated.total,
            "total_pages": paginated.pages,
            "current_page": paginated.page,
            "per_page": paginated.per_page,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
            "next_page": paginated.next_num,
            "prev_page": paginated.prev_num,
        },
    }
    return jsonify(response), 200


from shapely.geometry import Point


@town_halls_bp.route("/stops/<string:town_hall>", methods=["GET"])
def get_by_town_hall(town_hall):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    rs = TownHall.query.filter_by(slug=town_hall).first()
    if not rs:
        abort(404, f"The town hall '{town_hall}' not found!")

    town_halls_geojson = gpd.read_file(config.POLIGONS_GEOJSON_PATH)
    gdf_town_halls = town_halls_geojson[town_halls_geojson["NOMGEO"] == rs.name]

    polygon = gdf_town_halls.geometry.iloc[0]

    query = Stop.query.all()
    filtered_stops = []

    for stop in query:
        point = Point(stop.stop_lon, stop.stop_lat)
        if not polygon.contains(point):
            continue
        filtered_stops.append(stop)

    paginated = filtered_stops[(page - 1) * per_page : page * per_page]
    serialized = [stop.to_dict() for stop in paginated]

    if not serialized:
        abort(404, "No stops found in this area!")

    response = {
        "data": serialized,
        "pagination": {
            "total_items": len(filtered_stops),
            "total_pages": (len(filtered_stops) // per_page) + 1,
            "current_page": page,
            "per_page": per_page,
            "has_next": len(filtered_stops) > page * per_page,
            "has_prev": page > 1,
            "next_page": page + 1 if len(filtered_stops) > page * per_page else None,
            "prev_page": page - 1 if page > 1 else None,
        },
    }
    return jsonify(response), 200


def get_bounding_box(polygon_coords):
    from shapely.geometry import shape
    polygon = shape({"type": "Polygon", "coordinates": [polygon_coords]})
    return polygon.bounds
