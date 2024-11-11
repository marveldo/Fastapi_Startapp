from app.tokens.access import AccessToken
from app.tokens.refresh import Refreshtoken
from app.services import BaseServices
from app.db import get_db
from app.settings import settings
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .models import User
from fastapi import Depends
from jose import JWTError


security = HTTPBearer()

class UserService(BaseServices):
    
    @classmethod
    def authenticate_user(cls , email , password , db: Session) :
        user : User = User.objects.get(email = email , db=db)
        if user is None :
            raise HTTPException(status_code=401, detail={'message': 'Unauthorized'})
        if not user.check_password(password):
            raise HTTPException(status_code=401 , detail={'message': 'Username or password incorrect'})
        token = Refreshtoken.for_user(user , db=db)
        user_detail = user.email
        return {
            'access' : str(token.get('access')),
            'refresh' : str(token.get('refresh')),
            'user' : jsonable_encoder(user , exclude=['password'])
        }
    
    @classmethod
    def verify_authenticated_user(cls,credentials : HTTPAuthorizationCredentials = Depends(security), db : Session = Depends(get_db)) :
        token = credentials.credentials
        try :
            access = AccessToken(token)
        except JWTError :
            raise HTTPException(status_code=401 , detail={'detail' : 'Access Token not valid'})
        user = User.objects.get(db=db , id = access.payload.get('user_id'))
        if user is None :
            raise HTTPException(status_code=401 , detail={'detail' : 'Access Token not valid'})
        return user
    
    @classmethod 
    def blacklist_refresh_token(cls , refresh_token : str , db : Session) :
        try :
           refresh = Refreshtoken(refresh_token=refresh_token, db=db)
        except JWTError :
            raise HTTPException(status_code=400 , detail={'refresh token not valid or already blacklisted'})
        
        refresh.blacklist()

        return {
            'status' : 200,
            'message' : 'Token Blacklisted'
        }
    
    @classmethod
    def refresh_tokens(cls , refresh_token : str , db : Session):
        try : 
            refresh = Refreshtoken(db=db , refresh_token=refresh_token)
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=400 , detail='refresh token not valid')
        user : User = refresh.token_model.user
        

        if not settings.ROTATE_REFRESH_TOKENS :
           access_token = AccessToken.for_user(user)
           user_email = user.email
           token = {
               'access' : str(access_token),
                'user' : jsonable_encoder(user , exclude=['password'])
            }
        if settings.ROTATE_REFRESH_TOKENS :
            tokens = Refreshtoken.for_user(user , db=db)
            if settings.BLACKLIST_ON_ROTATION :
                refresh.blacklist()
            else :
                pass
            user_email = user.email
            token = {
                'access' : str(tokens.get('access')),
                'refresh' : str(tokens.get('refresh')),
                'user' : jsonable_encoder(user , exclude=['password'])
            }
        
        return token
        

    
        
    
        
        


    



