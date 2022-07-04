from sqlalchemy import create_engine
from sqlalchemy import orm as _orm

from interfaces import UoW
from repo import DBUoW
from mapper import registry
from domain import User


def some_service(uow: UoW):
    user = User(id=None, name="name", nickname="nick123")
    print(user)
    uow.users.add(user)
    print(user)
    print(list(uow.users.list()))
    assert user.id is not None
    assert uow.users.get(user.id) == user

    uow.rollback()
    assert uow.users.get(user.id) is None


def main():
    engine = create_engine("sqlite://", future=True)
    registry.metadata.create_all(engine)
    session = _orm.Session(engine)
    uow = DBUoW(session)
    try:
        some_service(uow)
        uow.commit()
    except Exception:
        uow.rollback()


if __name__ == "__main__":
    main()
