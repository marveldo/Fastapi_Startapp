from datetime import datetime
from typing import (Optional, Union,
                    List, Annotated, Dict,
                    Literal)

from pydantic import (BaseModel, EmailStr,
                      field_validator, ConfigDict,
                      StringConstraints,
                      model_validator)
from .validators import password_validator ,email_is_valid

class Login(BaseModel):
    email : EmailStr
    password : str

    @model_validator(mode='before')
    @classmethod
    def validate_email_passowrd(cls , values : dict) :
        email = values.get('email')
        password = values.get('password')

        password_validator(password)

        if not email_is_valid(email=email):
            raise ValueError('Email Invalid')
        
        return values

class Refresh(BaseModel):
    refresh_token : str

    
        
       



