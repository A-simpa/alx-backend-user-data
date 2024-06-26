#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add a user to the data-base"""
        new_user = User(email=email,
                        hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """filters user by keyword"""
        field = list(kwargs.keys())[0]
        if not (hasattr(User, field)):
            raise InvalidRequestError
        value = kwargs[field]
        query = self._session.query(User).filter(
            eval(f"User.{field}") == value)

        user = query.first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates a user by filtering for id"""
        try:
            user = self.find_user_by(id=user_id)
        except Exception:
            raise ValueError
        for attr, value in kwargs.items():
            if not (hasattr(user, attr)):
                raise ValueError
            exec(f"user.{attr} = value")

        self._session.commit()
