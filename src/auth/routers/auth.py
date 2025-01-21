from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from ..permissions import permissions
from ..schemas.client import ClientSchema, ClientCreateSchema, ClientLoginSchema
from ..schemas.operator import OperatorLoginSchema, OperatorCreateSchema, OperatorSchema
from ..schemas.token import TokenPairSchema, RefreshRequestSchema
from ..services.auth import AuthService
from ..services.token import TokenPairService

token_router = APIRouter(tags=["Auth"],
                         dependencies=[Depends(permissions.allowAnyAuthenticated)])

auth_router = APIRouter(tags=["Auth"],
                        dependencies=[Depends(permissions.allowAll)])


@auth_router.post('/register', status_code=status.HTTP_201_CREATED,
                  response_model=ClientSchema | OperatorSchema)
def register(payload: ClientCreateSchema | OperatorCreateSchema,
             service: AuthService = Depends()) -> ClientSchema | OperatorSchema:
    return service.register_user(payload)


@auth_router.post('/login')
def login(payload: ClientLoginSchema | OperatorLoginSchema,
          service: AuthService = Depends(),
          token_service: TokenPairService = Depends()) -> dict:
    authenticated_user: OperatorSchema | ClientSchema = service.authenticate_user(payload)
    token_pair: TokenPairSchema = token_service.generate_token_pair(authenticated_user)
    return {"user": token_pair.user,
            "access_token": token_pair.access_token,
            "refresh_token": token_pair.refresh_token}


@token_router.get('/logout')
def logout(response: Response) -> dict:
    # response.delete_cookie(key='refresh_token')
    return {"detail": "Successfully logged out"}


@token_router.post('/refresh')
def refresh(payload: RefreshRequestSchema,
            token_service: TokenPairService = Depends()) -> dict:
    refresh_token: str = payload.refresh_token
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь не авторизован")
    new_token_pair: TokenPairSchema = token_service.refresh_token_pair(refresh_token)
    return {"user": new_token_pair.user,
            "access_token": new_token_pair.access_token,
            "refresh_token": new_token_pair.refresh_token}
