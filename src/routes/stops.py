from flask import Blueprint, abort, jsonify, request

from src.models.stop import Stop

stops_bp = Blueprint("stops", __name__)


@stops_bp.route("/", methods=["GET"])
def get_all():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated = Stop.query.paginate(page=page, per_page=per_page, error_out=False)
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


@stops_bp.route("/<string:stop_id>")
def get_stop(stop_id):
    query = Stop.query.filter_by(stop_id=stop_id).first()
    if not query:
        abort(404, "Row not found!")

    return jsonify(query.to_dict()), 200
