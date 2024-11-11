from ..db import Base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func
)
from uuid_extensions import uuid7
from .Basemanager import BaseManager,Custommeta
from sqlalchemy.orm import Session



class BaseModel(Base , metaclass=Custommeta):
    
    __abstract__ = True
    

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid7()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    objects = BaseManager()

    def delete(self , db : Session):
        """Model method that deletes a model instance from the database

        Args:
            db (Session): database session
        """
        db.delete(self)
        db.commit()

    def save(self, db : Session):
        """Save method called on a model after saving it

        Args:
            db (Session): database session
        """
        db.commit()
        db.refresh(self)



