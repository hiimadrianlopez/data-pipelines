"""empty message

Revision ID: bec6a643138e
Revises: 
Create Date: 2024-12-31 00:23:38.350033

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "bec6a643138e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "agency",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agency_id", sa.Integer(), nullable=True),
        sa.Column("agency_name", sa.String(), nullable=True),
        sa.Column("agency_url", sa.String(), nullable=True),
        sa.Column("agency_timezone", sa.String(), nullable=True),
        sa.Column("agency_lang", sa.String(), nullable=True),
        sa.Column("agency_phone", sa.String(), nullable=True),
        sa.Column("agency_fare_url", sa.String(), nullable=True),
        sa.Column("agency_email", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("agency_id"),
    )
    op.create_table(
        "calendar",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.String(), nullable=False),
        sa.Column("monday", sa.Integer(), nullable=False),
        sa.Column("tuesday", sa.Integer(), nullable=False),
        sa.Column("wednesday", sa.Integer(), nullable=False),
        sa.Column("thursday", sa.Integer(), nullable=False),
        sa.Column("friday", sa.Integer(), nullable=False),
        sa.Column("saturday", sa.Integer(), nullable=False),
        sa.Column("sunday", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.String(length=8), nullable=False),
        sa.Column("end_date", sa.String(length=8), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("service_id"),
    )
    op.create_table(
        "calendar_date",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.String(), nullable=False),
        sa.Column("date", sa.String(length=8), nullable=False),
        sa.Column("exception_type", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("service_id"),
    )
    op.create_table(
        "feed_info",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("feed_publisher_name", sa.String(), nullable=False),
        sa.Column("feed_publisher_url", sa.String(), nullable=False),
        sa.Column("feed_lang", sa.String(), nullable=False),
        sa.Column("default_lang", sa.String(), nullable=True),
        sa.Column("feed_start_date", sa.String(length=8), nullable=False),
        sa.Column("feed_end_date", sa.String(length=8), nullable=False),
        sa.Column("feed_version", sa.Integer(), nullable=False),
        sa.Column("feed_contact_email", sa.String(), nullable=True),
        sa.Column("feed_contact_url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "route",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("route_id", sa.Integer(), nullable=False),
        sa.Column("agency_id", sa.Integer(), nullable=False),
        sa.Column("route_short_name", sa.String(), nullable=True),
        sa.Column("route_long_name", sa.String(), nullable=True),
        sa.Column("route_desc", sa.String(), nullable=True),
        sa.Column("route_type", sa.Integer(), nullable=False),
        sa.Column("route_url", sa.String(), nullable=True),
        sa.Column("route_color", sa.String(), nullable=True),
        sa.Column("route_text_color", sa.String(), nullable=True),
        sa.Column("route_sort_order", sa.Integer(), nullable=True),
        sa.Column("continuous_pickup", sa.String(), nullable=True),
        sa.Column("continuous_drop_off", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("route_id"),
    )
    op.create_table(
        "shape",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("shape_id", sa.Integer(), nullable=False),
        sa.Column("shape_pt_lat", sa.Float(), nullable=False),
        sa.Column("shape_pt_lon", sa.Float(), nullable=False),
        sa.Column("shape_pt_sequence", sa.Integer(), nullable=False),
        sa.Column("shape_dist_traveled", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stop",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stop_id", sa.String(), nullable=False),
        sa.Column("stop_code", sa.String(), nullable=True),
        sa.Column("stop_name", sa.String(), nullable=False),
        sa.Column("stop_desc", sa.String(), nullable=True),
        sa.Column("stop_lat", sa.Float(), nullable=False),
        sa.Column("stop_lon", sa.Float(), nullable=False),
        sa.Column("zone_id", sa.String(), nullable=True),
        sa.Column("stop_url", sa.String(), nullable=True),
        sa.Column("location_type", sa.Integer(), nullable=True),
        sa.Column("parent_station", sa.String(), nullable=True),
        sa.Column("stop_timezone", sa.String(), nullable=True),
        sa.Column("wheelchair_boarding", sa.Integer(), nullable=True),
        sa.Column("level_id", sa.String(), nullable=True),
        sa.Column("platform_code", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stop_time",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("trip_id", sa.String(), nullable=False),
        sa.Column("arrival_time", sa.String(), nullable=False),
        sa.Column("departure_time", sa.String(), nullable=False),
        sa.Column("stop_id", sa.String(), nullable=False),
        sa.Column("stop_sequence", sa.Integer(), nullable=False),
        sa.Column("stop_headsign", sa.String(), nullable=True),
        sa.Column("pickup_type", sa.Integer(), nullable=True),
        sa.Column("drop_off_type", sa.Integer(), nullable=True),
        sa.Column("continuous_pickup", sa.String(), nullable=True),
        sa.Column("continuous_drop_off", sa.String(), nullable=True),
        sa.Column("shape_dist_traveled", sa.Float(), nullable=True),
        sa.Column("timepoint", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "town_hall",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("slug", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("meta_data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "trip",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("route_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.String(), nullable=False),
        sa.Column("trip_id", sa.String(), nullable=False),
        sa.Column("trip_headsign", sa.String(), nullable=True),
        sa.Column("trip_short_name", sa.String(), nullable=True),
        sa.Column("direction_id", sa.Integer(), nullable=False),
        sa.Column("block_id", sa.String(), nullable=True),
        sa.Column("shape_id", sa.Integer(), nullable=False),
        sa.Column("wheelchair_accessible", sa.Integer(), nullable=True),
        sa.Column("bikes_allowed", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trip_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("trip")
    op.drop_table("town_hall")
    op.drop_table("stop_time")
    op.drop_table("stop")
    op.drop_table("shape")
    op.drop_table("route")
    op.drop_table("feed_info")
    op.drop_table("calendar_date")
    op.drop_table("calendar")
    op.drop_table("agency")
    # ### end Alembic commands ###
