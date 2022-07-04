from typing import Optional, Iterable
import abc
from domain import User


class UserRepo(abc.ABC):
    @abc.abstractmethod
    def list(self) -> Iterable[User]:
        ...

    @abc.abstractmethod
    def get(self, id) -> Optional[User]:
        ...

    @abc.abstractmethod
    def add(self, user: User):
        ...


class UoW(abc.ABC):
    @abc.abstractproperty
    def users(self) -> UserRepo:
        ...

    @abc.abstractmethod
    def commit(self):
        ...

    @abc.abstractmethod
    def rollback(self):
        ...
