from datetime import datetime

from pydantic import BaseModel

from .client import ClientSchema
from .operator import OperatorSchema
from ...settings import settings


class TokenSchema(BaseModel):
    expires_in: int
    token_type: str


class AccessTokenSchema(TokenSchema):
    expires_in: int = settings.jwt_access_token_expires
    token_type: str = 'access'


class RefreshTokenSchema(TokenSchema):
    expires_in: int = settings.jwt_refresh_token_expires
    token_type: str = 'refresh'


class TokenPairSchema(BaseModel):
    """
    Пара access и refresh токенов и модель пользователя, для которого она генерится

    Attributes
    ----------
    user : OperatorSchema | ClientSchema
        pydantic модель пользователя
    access_token : str
        закодированный access токен
    refresh_token : str
        закодированный refresh_токен
    """

    user: OperatorSchema | ClientSchema
    access_token: str
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    """
    Содержимое (payload) jwt токена

    Attributes
    ----------
    token_type : str
        тип токена
    iat : datetime
        дата создания токена
    exp : datetime
        дата истечения срока жизни токена
    user_id : int
        id пользователя
    user_role: str
        роль пользователя
    """
    token_type: str
    iat: datetime
    exp: datetime
    user_id: int
    user_role: str


class TokenPayloadClientSchema(TokenPayloadSchema):
    """
    Содержимое (payload) jwt токена для клиента

    Attributes
    ----------
    user_login_number: str | None
        номер пользователя, с которым он залогинился в последний раз
    """
    user_login_number: str = None

    @classmethod
    def from_payload(cls, payload: TokenPayloadSchema, number: str):
        return TokenPayloadClientSchema(
            token_type=payload.token_type,
            iat=payload.iat,
            exp=payload.exp,
            user_id=payload.user_id,
            user_role=payload.user_role,
            user_login_number=number
        )


class TokenPayloadOperatorSchema(TokenPayloadSchema):
    """
    Содержимое (payload) jwt токена для оператора

    Attributes
    ----------
    user_email: str = None
        email оператора
    """
    user_email: str = None

    @classmethod
    def from_payload(cls, payload: TokenPayloadSchema, email: str):
        return TokenPayloadOperatorSchema(
            token_type=payload.token_type,
            iat=payload.iat,
            exp=payload.exp,
            user_id=payload.user_id,
            user_role=payload.user_role,
            user_email=email
        )

