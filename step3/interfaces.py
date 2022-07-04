from typing import Optional, Iterable, Generic, TypeVar
import abc
from domain import User, Tweet

T = TypeVar("T")


class _Repo(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def list(self) -> Iterable[T]:
        ...

    @abc.abstractmethod
    def get(self, id) -> Optional[T]:
        ...

    @abc.abstractmethod
    def add(self, user: T):
        ...


class UserRepo(_Repo[User]):
    pass


class TweetRepo(_Repo[Tweet]):
    pass


class UoW(abc.ABC):
    @abc.abstractproperty
    def users(self) -> UserRepo:
        ...

    @abc.abstractproperty
    def tweets(self) -> TweetRepo:
        ...

    @abc.abstractmethod
    def commit(self):
        ...

    @abc.abstractmethod
    def rollback(self):
        ...
