from sqlalchemy import (
    Column,
    String,
    Boolean,
    text,
    ForeignKey
)
from sqlalchemy.orm import Session , relationship
from app.models.BaseModel import BaseModel
from app.models.Basemanager import BaseManager
from .hashers import hash_password , verify_password


class UserManager(BaseManager):

    def create(self, db : Session, **kwargs):
        if 'password' in kwargs:
            password = kwargs.pop('password')  # Get and remove the password
            hashed_password = hash_password(password)  # Hash the password
            kwargs['password'] = hashed_password  # Add the hashed password back to kwargs
        
        return super().create(db=db, **kwargs)
    
    def create_super_user(self, db: Session, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superadmin', True)
        kwargs.setdefault('is_verified', True)
        
        return self.create( db=db, **kwargs)



class User(BaseModel) :

    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, server_default=text("true"))
    is_superadmin = Column(Boolean, server_default=text("false"))
    is_deleted = Column(Boolean, server_default=text("false"))
    is_verified = Column(Boolean, server_default=text("false"))

    token = relationship(
        "OutStandingTokens", back_populates="user"
    )

    def check_password(self, new_password):
        return verify_password(new_password , self.password)
    
    
    objects = UserManager()
    



    

