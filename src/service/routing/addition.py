from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.service.services.common_service import Service


addition_router = APIRouter(tags=["Addition"])





