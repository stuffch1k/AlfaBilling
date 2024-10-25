from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from ..permissions import permissions
from ..schemas.client import ClientSchema, ClientCreateSchema, ClientLoginSchema
from ..schemas.models import Operator, Client
from ..schemas.operator import OperatorLoginSchema, OperatorCreateSchema, OperatorSchema
from ..schemas.token import TokenPairSchema
from ..services.auth import AuthService
from ..services.token import TokenPairService

token_router = APIRouter(tags=["Auth"],
                         dependencies=[Depends(permissions.allowOperator)])

auth_router = APIRouter(tags=["Auth"],
                        dependencies=[Depends(permissions.allowAll)])


@auth_router.post('/register', status_code=status.HTTP_201_CREATED,
                  response_model=ClientSchema | OperatorSchema)
def register(payload: ClientCreateSchema | OperatorCreateSchema,
             service: AuthService = Depends()) -> ClientSchema | OperatorSchema:
    return service.register_user(payload)


@auth_router.post('/login')
def login(payload: ClientLoginSchema | OperatorLoginSchema,
          response: Response,
          service: AuthService = Depends(),
          token_service: TokenPairService = Depends()) -> dict:
    authenticated_user: Client | Operator = service.authenticate_user(payload)
    token_pair: TokenPairSchema = token_service.generate_token_pair(authenticated_user)
    response.set_cookie(key='refresh_token', value=token_pair.refresh_token,
                        max_age=3 * 24 * 60 * 60, httponly=True)
    return {"user": token_pair.user,
            "access_token": token_pair.access_token}


@token_router.get('/logout')
def logout(response: Response) -> dict:
    response.delete_cookie(key='refresh_token')
    return {"detail": "Successfully logged out"}


@token_router.get('/refresh')
def refresh(request: Request,
            response: Response,
            token_service: TokenPairService = Depends()) -> dict:
    refresh_token: str = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь не авторизован")
    new_token_pair: TokenPairSchema = token_service.refresh_token_pair(refresh_token)
    response.set_cookie(key='refresh_token', value=new_token_pair.refresh_token,
                        max_age=3 * 24 * 60 * 60, httponly=True)
    return {"user": new_token_pair.user,
            "access_token": new_token_pair.access_token}
