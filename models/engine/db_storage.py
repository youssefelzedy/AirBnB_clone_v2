#!/usr/bin/python3
"""This module defines a class to manage DB storage for hbnb clone"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class DBStorage:
    """This class manages storage of hbnb models in the DataBase

    Attributes:
        __engine: current sqlalchemy engine
        __session: current sqlalchemy session"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance"""
        DBStorage.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                           format(getenv("HBNB_MYSQL_USER"),
                                                  getenv("HBNB_MYSQL_PWD"),
                                                  getenv("HBNB_MYSQL_HOST"),
                                                  getenv("HBNB_MYSQL_DB")),
                                           pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        '''
        query for all objects on the current database session
        '''
        classes = {
            "City": City,
            "State": State,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity,
        }
        result = {}
        query_rows = []

        if cls:
            '''Query for all objects belonging to cls'''
            if type(cls) is str:
                cls = eval(cls)
            query_rows = self.__session.query(cls)
            for obj in query_rows:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                result[key] = obj
            return result
        else:
            '''Query for all types of objects'''
            for name, value in classes.items():
                query_rows = self.__session.query(value)
                for obj in query_rows:
                    key = '{}.{}'.format(name, obj.id)
                    result[key] = obj
            return result

    def new(self, obj):
        """ """
        self.__session.add(obj)

    def save(self):
        """ """
        self.__session.commit()

    def delete(self, obj=None):
        """ """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ """
        from models.base_model import Base

        Base.metadata.create_all(DBStorage.__engine)
        Session = scoped_session(sessionmaker(bind=DBStorage.__engine,
                                              expire_on_commit=False))
        DBStorage.__session = Session()

    def close(self):
        """ """
        self.__session.close()
