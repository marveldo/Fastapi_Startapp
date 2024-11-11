from sqlalchemy.orm import Session , Query
from typing import TypeVar , Type , Generic , Optional , List
import logging
from sqlalchemy.ext.declarative import DeclarativeMeta


T = TypeVar("T")

class BaseManager(Generic[T]) :

    def __init__(self , model = None):
        self.model = model
    
    def __set_name__(self, owner, name):
        if self.model == None :
            self.model = owner

    def query(self , db : Session) -> Query :
        """Returns back the query object for complex queries that default base manager class cant handle

        Args:
            db (Session): database session

        Returns:
            Query: _description_
        """
        return db.query(self.model)

    def get(self,  db : Session , **kwargs) -> Optional[T] :
        """Gets an object by attribute of the model class

        Args:
            db (Session): Db session

        Returns:
            Optional[T]: returns the db object
        """
        return db.query(self.model).filter_by(**kwargs).first()

    def all(self , db : Session) -> List[T]:
        """returns all the instances of a model in the database

        Args:
            db (Session): database session

        Returns:
            List[T]: List of all the models
        """
        return db.query(self.model).all()
    
    def create(self , db : Session, **kwargs ):

        """Object manager that creates a new instance of a model in the database and returns the created instance

        Returns:
            _type_: The Model Object
        """
        obj = self.model(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def get_or_create(self, db : Session , **kwargs):
        """Gets a model instance then creates it if the object doesnt exist

        Args:
            db (Session): database Session

        Returns:
            _type_: Model Type
        """
        created = False
        obj = db.query(self.model).filter_by(**kwargs).first()
        if not obj :
            obj = self.model(**kwargs)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            created = True
        return created , obj
    
    def paginate_model(self , db : Session , limit : int = 10, offset : int = 0 ,**kwargs):
        """Object manager that paginates a model can be overwritten if neccessary

        Args:
            db (Session): database Session
            limit (int, optional): size of data returned Defaults to 10.
            offset (int, optional): instance that should be started from Defaults to 0.

        Returns:
            _type_: object with the limit offset and list of model instances
        """
        objs = db.query(self.model).offset(offset).limit(limit).all()

        return {
            'offset' : offset,
            'limit' : limit,
            'data' : objs
         }

class Custommeta(DeclarativeMeta):

    """Overwriting the Declarative meta in Base class to pass Basemanager into any model created with this meta class    
    """

    def __new__(cls, name , bases , dct):
        new_class = super().__new__(cls, name , bases, dct)
        if '__tablename__' in dct  :
            if 'objects' not in dct :
                new_class.objects = BaseManager(model=new_class)
            else :
                pass
        return new_class







