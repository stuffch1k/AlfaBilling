from fastapi import APIRouter, Depends

from src.auth.permissions import permissions
from src.number.schemas.number import AddServiceSchema
from src.number.services.number import NumberService

activated_router = APIRouter(tags=["Activated service"])

@activated_router.post("/")
def add_service(schema: AddServiceSchema,
                service: NumberService = Depends(),
                user = Depends(permissions.allowAll)):
    return service.add_service(schema)

