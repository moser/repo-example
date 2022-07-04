# domain.py
from typing import Optional
import dataclasses as _dc


@_dc.dataclass
class User:
    id: int
    name: str
    nickname: Optional[str]


# mapper.py
import sqlalchemy as _sa
from sqlalchemy import orm as _orm

# from domain import User

registry = _orm.registry()

user_table = _sa.Table(
    "user",
    registry.metadata,
    _sa.Column("id", _sa.Integer, primary_key=True),
    _sa.Column("name", _sa.String(50), nullable=False),
    _sa.Column("nickname", _sa.String(12), nullable=True),
)

registry.map_imperatively(User, user_table)

# repo.py
from typing import Optional, Iterable

# from domain import User
class UserRepo:
    def __init__(self, session):
        self.session = session

    def list(self) -> Iterable[User]:
        yield from self.session.query(User).all()

    def get(self, id) -> Optional[User]:
        return self.session.get(User, id)

    def add(self, user: User):
        self.session.add(user)
        self.session.flush()
        # flush here makes sure
        #   - to raise DB errors (null, foreign key missing) ASAP
        #   - DB default (eg PK sequences) are resolved ASAP


# main.py
from sqlalchemy import orm as _orm

# from repo import UserRepo
# from mapper import registry
# from domain import User
def main():
    from sqlalchemy import create_engine

    engine = create_engine("sqlite://", future=True)
    registry.metadata.create_all(engine)
    session = _orm.Session(engine)

    user = User(id=None, name="name", nickname="nick123")
    print(user)
    repo = UserRepo(session)
    repo.add(user)
    print(user)
    print(list(repo.list()))
    assert user.id is not None
    assert repo.get(user.id) == user

    session.rollback()
    assert repo.get(user.id) is None


if __name__ == "__main__":
    main()
