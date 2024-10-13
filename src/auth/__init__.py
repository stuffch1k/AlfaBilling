from fastapi import APIRouter
# from .routers.client import router as client_router
# from .routers.operator import router as operator_router
from .routers.auth import token_router
from .routers.client import client_router
from .routers.operator import operator_router

router = APIRouter(prefix="/auth", tags=["Auth"])
router.include_router(operator_router)
router.include_router(client_router)
router.include_router(token_router)
