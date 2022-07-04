import sqlalchemy as _sa
from sqlalchemy import orm as _orm

from domain import User, Tweet

registry = _orm.registry()

user_table = _sa.Table(
    "user",
    registry.metadata,
    _sa.Column("id", _sa.Integer, primary_key=True),
    _sa.Column("name", _sa.String(50), nullable=False),
    _sa.Column("nickname", _sa.String(12), nullable=True),
)

registry.map_imperatively(User, user_table)

tweet_table = _sa.Table(
    "tweet",
    registry.metadata,
    _sa.Column("id", _sa.Integer, primary_key=True),
    _sa.Column("text", _sa.String(140), nullable=False),
    _sa.Column(
        "_author_id", _sa.Integer, _sa.ForeignKey(user_table.c.id), nullable=False
    ),
)

registry.map_imperatively(
    Tweet, tweet_table, properties={"author": _orm.relationship(User, backref="tweets")}
)
