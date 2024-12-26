from datetime import datetime

from flask import Blueprint, abort, jsonify, request

from src.models import db
from src.models.calendar import Calendar
from src.models.shape import Shape
from src.models.trip import Trip

services_bp = Blueprint("services", __name__)


@services_bp.route("/")
def get_service():
    current_day = datetime.now().strftime("%A").lower()
    day_column = getattr(Calendar, current_day)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = Calendar.query.filter(day_column == 1)
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    serialized = [cal.to_dict() for cal in paginated.items]
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


@services_bp.route("/<string:service_id>/locations", methods=["GET"])
def get_location_by_service_id(service_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = (
        db.session.query(Trip.service_id, Shape.shape_pt_lat, Shape.shape_pt_lon)
        .join(Shape, Trip.shape_id == Shape.shape_id)
        .filter(Trip.service_id == service_id)
    )

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    results = [
        {"service_id": row.service_id, "lat": row.shape_pt_lat, "lon": row.shape_pt_lon}
        for row in paginated.items
    ]

    if not results:
        abort(404, description=f"Information not found '{service_id}'.!")

    response = {
        "data": results,
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


@services_bp.route("/day/<string:day_of_week>")
def get_service_by_day(day_of_week):
    days_of_week = (
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    )
    if day_of_week.lower() not in days_of_week:
        abort(404, description=f"Please give a correct day of week: {days_of_week}")

    day_column = getattr(Calendar, day_of_week.lower())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = Calendar.query.filter(day_column == 0)
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    serialized = [cal.to_dict() for cal in paginated.items]
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


@services_bp.route("/day")
def get_service_by_current_day():
    current = datetime.today().strftime("%A").lower()
    day_column = getattr(Calendar, current)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    query = Calendar.query.filter(day_column == 0)
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    serialized = [cal.to_dict() for cal in paginated.items]
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
