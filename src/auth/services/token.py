import base64
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from starlette import status

from .client import AuthClientService
from .operator import AuthOperatorService
from src.auth.schemas.models import Operator, Client
from ..schemas.client import ClientSchema
from ..schemas.operator import OperatorSchema
from ..schemas.token import TokenPairSchema, TokenSchema, AccessTokenSchema, RefreshTokenSchema
from ...settings import settings


class TokenPairService:

    def __init__(self, client_service: AuthClientService = Depends(AuthClientService),
                 operator_service: AuthOperatorService = Depends(AuthOperatorService)):
        self.client_service = client_service
        self.operator_service = operator_service

    def refresh_token_pair(self, refresh_token: str) -> TokenPairSchema:
        token_data: dict = self.validate_token(refresh_token)
        if token_data["user_role"] == "operator":
            user: Operator = self.operator_service.get_operator_by_id(token_data['user_id'])
        else:
            user: Client = self.client_service.get_client_by_id(token_data['user_id'])
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Пользователь не найден')
        return self.generate_token_pair(user)

    def generate_token_pair(self, user: Operator | Client) -> TokenPairSchema:
        if isinstance(user, Operator):
            user_data = OperatorSchema.model_validate(user)
        else:
            user_data = ClientSchema.model_validate(user)
        access_token: str = self.generate_token(user_data, token_schema=AccessTokenSchema())
        refresh_token: str = self.generate_token(user_data, token_schema=RefreshTokenSchema())
        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)

    def generate_token(self, user_data: OperatorSchema | ClientSchema, token_schema: TokenSchema) -> str:
        payload: dict = self.generate_payload(user_data, token_schema)
        token: str = jwt.encode(
            payload,
            key=base64.b64decode(settings.jwt_secret).decode('utf-8'),
            algorithm=settings.jwt_algorithm,
        )
        return token

    def validate_token(self, token: str) -> dict:
        try:
            payload: dict = jwt.decode(
                token=token,
                key=base64.b64decode(settings.jwt_secret).decode('utf-8'),
                algorithms=settings.jwt_algorithm,
            )
            if datetime.fromtimestamp(payload['exp']) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired"
                )
            return payload

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Token not valid')


    @classmethod
    def generate_payload(cls, user_data: OperatorSchema | ClientSchema, token_schema: TokenSchema) -> dict:
        now: datetime = datetime.now(timezone.utc)
        payload: dict = {
            "token_type": token_schema.token_type,
            "iat": now,
            "exp": now + timedelta(minutes=token_schema.expires_in),
            "user_id": user_data.Id,
            "user_role": user_data.Role
        }
        return payload



