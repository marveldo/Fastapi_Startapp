from jose import jwt , JWTError
from users.models import User
from ..settings import settings
from datetime import  datetime

class AccessToken :
    """Method that manages the access token
    """
    def __init__(self, access_token : str = None) :
        """Initializes the access Token class while verifying the access Token

        Args:
            access_token (str, optional): Access Token passed in Defaults to None.

        Raises:
            JWTError: Raises JWTERROR on invalid access token
            JWTError: Raises JWTERROR on access token without a token_type
            JWTError: Raises JWTERROR on token expiry
        """
        self.token = access_token 
        if self.token is not None :
            try :
                self.payload = jwt.decode(self.token , settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                expiry = self.payload.get('exp')
                if expiry is None or datetime.utcnow() > datetime.fromtimestamp(expiry):
                    raise JWTError
                token_type = self.payload.get('token_type')
                if token_type != 'access':
                    raise JWTError
            except JWTError :
                raise JWTError
        
        

    @classmethod
    def for_user(cls, user : User):
        """method that generates the access token for user

        Args:
            user (User): User model

        Returns:
            str : the encoded token
        """
        payload = {'user_id' : user.id , 'email' : user.email , 'token_type' : 'access'}
        expires = datetime.utcnow() + settings.ACCESS_TOKEN_LIFETIME
        payload.update({'exp' : expires})
        return jwt.encode(payload , settings.SECRET_KEY , algorithm= settings.ALGORITHM)