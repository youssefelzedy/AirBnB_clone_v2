#!/usr/bin/python3
"""This module defines a class to manage DB storage for hbnb clone"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from os import getenv

class DBStorage:
    """the db storage class
    
    Attributes:
        __engine: current sqlalchemy engine
        __session: current sqlalchemy session"""
        
    __engine = None
    __session = None    
    
    def __init__(self):
        """Initialize a new DBStorage instance"""
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User
        
        DBStorage.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(DBStorage.__engine)
            
    def all(self, cls=None):
        
        results = {}
        
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User
        
        if cls is None:
            classes = [Amenity, City, Place, Review, State, User]
        else:
            classes = [cls]
            
        for class_obj in classes:
            objects = self.__session.query(class_obj).all()
            for obj in objects:
                results['{}.{}'.
                        format(obj.to_dict()['__class__'], obj.id)] = obj
                
        return results
    
    def new(self, obj):
        """Add obj to the current database session"""
        self.__session.add(obj)
        
    def save(self):
        """Commit all changes to the current database session"""
        self.__session.commit()
        
    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)
            
    def reload(self):
        """Create all tables in the database and initialize a new session"""
        
        Base.metadata.create_all(DBStorage.__engine)
        Session = scoped_session(sessionmaker(bind=DBStorage.__engine,
                                              expire_on_commit=False))
        DBStorage.__session = Session()
        
    def close(self):
        """Close the current session"""
        self.__session.close()
            
        
    
    