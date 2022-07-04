from sqlalchemy import create_engine
from sqlalchemy import orm as _orm

from interfaces import UoW
from repo import DBUoW
from mapper import registry
from domain import User, Tweet


def some_service(uow: UoW):
    user = User(id=None, name="name", nickname="nick123")
    uow.users.add(user)
    uow.tweets.add(Tweet(id=None, text="I am not Jack", author=user))

    print(user)
    print(user.tweets)


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
        raise


if __name__ == "__main__":
    main()
