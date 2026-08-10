import sqlalchemy as sa

engine = sa.create_engine("sqlite:///linemetrics.db", connect_args={"check_same_thread": False})
metadata = sa.MetaData()

readings = sa.Table(
    "readings", metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("reading_id", sa.String, nullable=False),   # from gateway; NOT unique-constrained
    sa.Column("line_id", sa.String, nullable=False),
    sa.Column("ts", sa.String, nullable=False),           # ISO UTC
    sa.Column("cycle_count", sa.Integer, nullable=False),
    sa.Column("reject_count", sa.Integer, nullable=False),
    sa.Column("downtime_minutes", sa.Float, nullable=False, default=0.0),
)

plan = sa.Table(
    "plan", metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("line_id", sa.String, nullable=False),
    sa.Column("date", sa.String, nullable=False),          # production date YYYY-MM-DD
    sa.Column("planned_minutes", sa.Float, nullable=False),
    sa.Column("ideal_cycle_time", sa.Float, nullable=False),  # minutes per piece
)


def init_db() -> None:
    metadata.create_all(engine)
