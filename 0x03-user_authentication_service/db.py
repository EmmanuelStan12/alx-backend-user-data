#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

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
        """Adds a user to the database
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        except Exception:
            self._session.rollback()
        return None

    def find_user_by(self, **kwargs) -> User:
        """Find the first user that matches the args.
        """
        valid_columns = User.__table__.columns.keys()
        invalid_keys = [key for key in kwargs if key not in valid_columns]

        if invalid_keys:
            raise InvalidRequestError

        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs):
        """Update a user's attributes in the database.
        """
        user = self.find_user_by(id=user_id)

        valid_columns = User.__table__.columns.keys()
        invalid_keys = [key for key in kwargs if key not in valid_columns]
        if invalid_keys:
            raise ValueError
        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
