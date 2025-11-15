from fastapi import APIRouter
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.auth import router as auth_router


api_router = APIRouter(prefix="/api/v1")

routers = [user_router, auth_router]

for router in routers:
    api_router.include_router(router)
