from fastapi import APIRouter
from users.views import user_router

api_main_route = APIRouter(prefix='/api/v1')
api_main_route.include_router(user_router)