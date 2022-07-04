from typing import Optional, Iterable, Generic, TypeVar, ClassVar, Type


from interfaces import TweetRepo, UserRepo, UoW
from domain import User, Tweet

T = TypeVar("T")


class _DBRepo(Generic[T]):
    model_type: ClassVar[Type[T]]

    def __init__(self, session):
        self.session = session

    def list(self) -> Iterable[T]:
        yield from self.session.query(self.model_type).all()

    def get(self, id) -> Optional[T]:
        return self.session.get(self.model_type, id)

    def add(self, user: T):
        self.session.add(user)
        self.session.flush()
        # flush here makes sure
        #   - to raise DB errors (null, foreign key missing) ASAP
        #   - DB default (eg PK sequences) are resolved ASAP


class DBUserRepo(_DBRepo[User], UserRepo):
    model_type = User


class DBTweetRepo(_DBRepo[Tweet], TweetRepo):
    model_type = Tweet


class DBUoW(UoW):
    def __init__(self, session):
        self.session = session

    @property
    def users(self) -> UserRepo:
        return DBUserRepo(self.session)

    @property
    def tweets(self) -> TweetRepo:
        return DBTweetRepo(self.session)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
