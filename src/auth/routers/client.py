from fastapi import APIRouter
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from ..schemas.token import TokenPairSchema
from ...models import Client
from ..services.token import TokenPairService
from ..schemas.client import ClientSchema, ClientCreateSchema, ClientLoginSchema
from ..services.client import AuthClientService

client_router = APIRouter(prefix="/client/jwt")


@client_router.post('/register', status_code=status.HTTP_201_CREATED,
                    response_model=ClientSchema)
def register_client(payload: ClientCreateSchema,
                    service: AuthClientService = Depends()) -> ClientSchema:
    return service.register_client(payload)


@client_router.post('/login')
def login_client(payload: ClientLoginSchema,
                 response: Response,
                 service: AuthClientService = Depends(),
                 token_service: TokenPairService = Depends()) -> dict:
    authenticated_client: Client = service.authenticate_client(payload)
    token_pair: TokenPairSchema = token_service.generate_token_pair(authenticated_client)
    response.set_cookie(key='refresh_token', value=token_pair.refresh_token,
                        max_age=3 * 24 * 60 * 60, httponly=True)
    return {"access_token": token_pair.access_token}