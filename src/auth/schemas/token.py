from pydantic import BaseModel
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
    access_token: str
    refresh_token: str
