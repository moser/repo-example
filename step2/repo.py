from typing import Optional, Iterable

from interfaces import UserRepo, UoW
from domain import User


class DBUserRepo(UserRepo):
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


class DBUoW(UoW):
    def __init__(self, session):
        self.session = session

    @property
    def users(self) -> UserRepo:
        return DBUserRepo(self.session)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
