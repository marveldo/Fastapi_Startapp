from fastapi import APIRouter , status , Depends
from app.db import get_db
from .models import User
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .services import UserService
from .schema import Login , Refresh
from app.tokens.models import OutStandingTokens

user_router = APIRouter(prefix='/users', tags=['User'])


@user_router.get(path='/',status_code=status.HTTP_200_OK)
async def get_all_users(db : Session = Depends(get_db)):
    users = User.objects.all(db=db)
    return {
        'status': status.HTTP_200_OK,
        'message' : 'Users Retrieval Successful',
        'data' : jsonable_encoder(users , exclude=['password'])
    }

@user_router.post('/auth/login/', status_code=status.HTTP_200_OK)
async def login_user(request_data : Login ,db : Session = Depends(get_db)) :
    return UserService.authenticate_user(email = request_data.email, password =request_data.password , db=db)


@user_router.get('/current/', status_code=status.HTTP_200_OK)
async def get_current_user(db : Session = Depends(get_db),current_user : User = Depends(UserService.verify_authenticated_user)):
    return jsonable_encoder(current_user, exclude=['password'])

@user_router.post('/auth/refresh/', status_code=200)
async def refresh_access_token(refresh : Refresh,db : Session = Depends(get_db)) :
    return UserService.refresh_tokens(refresh_token=refresh.refresh_token , db=db)


@user_router.post('/auth/logout/', status_code=status.HTTP_200_OK)
async def blacklist_token(data : Refresh ,db : Session = Depends(get_db)):
    return UserService.blacklist_refresh_token(refresh_token=data.refresh_token , db=db)

    