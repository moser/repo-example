import sqlalchemy as _sa
from sqlalchemy import orm as _orm

from domain import User

registry = _orm.registry()

user_table = _sa.Table(
    "user",
    registry.metadata,
    _sa.Column("id", _sa.Integer, primary_key=True),
    _sa.Column("name", _sa.String(50), nullable=False),
    _sa.Column("nickname", _sa.String(12), nullable=True),
)

registry.map_imperatively(User, user_table)
