from .models import OutStandingTokens , BlacklistedTokens
from datetime import datetime
from users.models import User
from ..settings import settings
from sqlalchemy.orm import Session
from jose import jwt , JWTError
from .access import AccessToken

class Refreshtoken :

    def __init__(self, db : Session , refresh_token : str = None):
        """ Initializes the refresh token class and verifies the refresh token

        Args:
            db (Session): database session
            refresh_token (str, optional): refresh token passed into the class. Defaults to None.

        Raises:
            JWTError: Token doesnt exist in database
            JWTError: Token is blacklisted
            JWTError: Token has expired
        """
        self.db= db
        self.refresh_token = refresh_token

        if self.refresh_token is not None :
            token : OutStandingTokens = OutStandingTokens.objects.get(db= self.db , token = self.refresh_token )
            if token is None :
                raise JWTError({'detail': 'Invalid Token'})
            
            elif BlacklistedTokens.objects.get(db=self.db , token = self.refresh_token) is not None :
                raise JWTError({'detail': 'Token has been blacklisted'})
            
            elif datetime.utcnow() > token.expires_in :
                token.delete(db = self.db)
                raise JWTError({'detail' : 'Token has expired'})
            
            self.token_model = token 

            
    @classmethod
    def for_user(cls , user : User, db : Session):
        """Generates a new refesh token and access token for user

        Args:
            user (User): User
            db (Session): database session

        Returns:
            dict: access and refresh tokens
        """
        access_token  = AccessToken.for_user(user)
        payload = {'user_id' : user.id , 'email' : user.email , 'first_name' : user.first_name , 'token_type' : 'refresh'}
        expires = datetime.utcnow() + settings.REFRESH_TOKEN_LIFETIME
        payload.update({'exp' : expires})
        refresh_token = jwt.encode(payload , settings.SECRET_KEY , algorithm= settings.ALGORITHM)
        OutStandingTokens.objects.create(token = refresh_token , expires_in = expires, user=user, db=db )
        return  {
            'access' : access_token ,
            'refresh' : refresh_token
        }
    
    def blacklist(self) :

        self.token_model.delete(db = self.db)

        BlacklistedTokens.objects.create(token = self.refresh_token , db=self.db)

        self.token_model = None

        self.refresh_token = None



            
            
            

            
            
            



        
    