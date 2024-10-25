from fastapi import APIRouter
from .routers.auth import token_router, auth_router
from .routers.user import user_router

router = APIRouter(prefix="/auth/jwt")
router.include_router(token_router)
router.include_router(auth_router)
router.include_router(user_router)
