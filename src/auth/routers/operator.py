from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from ...models import Operator
from ..services.token import TokenPairService
from ..services.operator import AuthOperatorService
from ..schemas.operator import OperatorSchema, OperatorCreateSchema, OperatorLoginSchema
from ..schemas.token import TokenPairSchema

operator_router = APIRouter(prefix="/operator/jwt")


@operator_router.post('/register', status_code=status.HTTP_201_CREATED,
                      response_model=OperatorSchema)
def register_operator(payload: OperatorCreateSchema,
                      service: AuthOperatorService = Depends()) -> OperatorSchema:
    return service.register_operator(payload)


@operator_router.post('/login')
def login_operator(payload: OperatorLoginSchema,
                   response: Response,
                   service: AuthOperatorService = Depends(),
                   token_service: TokenPairService = Depends()) -> dict:
    authenticated_operator: Operator = service.authenticate_operator(payload)
    token_pair: TokenPairSchema = token_service.generate_token_pair(authenticated_operator)
    response.set_cookie(key='refresh_token', value=token_pair.refresh_token,
                        max_age=3 * 24 * 60 * 60, httponly=True)
    return {"access_token": token_pair.access_token}
