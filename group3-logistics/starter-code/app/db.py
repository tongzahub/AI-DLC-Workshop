import sqlalchemy as sa

engine = sa.create_engine("sqlite:///parceltrack.db", connect_args={"check_same_thread": False})
metadata = sa.MetaData()

parcels = sa.Table(
    "parcels", metadata,
    sa.Column("id", sa.String, primary_key=True),          # e.g. TEX-2026-000123
    sa.Column("merchant_id", sa.String, nullable=False),   # M-100 etc.
    sa.Column("recipient_name", sa.String, nullable=False),
    sa.Column("recipient_phone", sa.String, nullable=False),
    sa.Column("address", sa.String, nullable=False),
    sa.Column("district", sa.String, nullable=False),
    sa.Column("cod_amount", sa.Float, nullable=False, default=0.0),  # 0.0 = not COD
    sa.Column("status", sa.String, nullable=False, default="CREATED"),
    sa.Column("rider_id", sa.String, nullable=True),
    sa.Column("created_at", sa.String, nullable=False),
    sa.Column("updated_at", sa.String, nullable=False),
)

status_history = sa.Table(
    "status_history", metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("parcel_id", sa.String, nullable=False),
    sa.Column("status", sa.String, nullable=False),
    sa.Column("note", sa.String, nullable=True),
    sa.Column("at", sa.String, nullable=False),
)

cod_collections = sa.Table(
    "cod_collections", metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("parcel_id", sa.String, nullable=False),
    sa.Column("rider_id", sa.String, nullable=False),
    sa.Column("amount", sa.Float, nullable=False),
    sa.Column("collected_at", sa.String, nullable=False),
)


def init_db() -> None:
    metadata.create_all(engine)
