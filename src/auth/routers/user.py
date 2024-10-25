from fastapi import APIRouter, Depends
from ..permissions import permissions
from ..schemas.client import ClientSchema
from ..schemas.operator import OperatorSchema
from ..services.user import get_current_user

user_router = APIRouter(tags=["User"],
                        dependencies=[Depends(permissions.allowAnyAuthenticated)])


@user_router.get('/user')
def get_current_user(user: OperatorSchema | ClientSchema = Depends(get_current_user)) \
        -> OperatorSchema | ClientSchema:
    return user
