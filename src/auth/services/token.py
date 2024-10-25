import base64
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from starlette import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from ..services.auth import AuthService
from ..schemas.models import Operator, Client
from ..schemas.client import ClientSchema
from ..schemas.operator import OperatorSchema
from ..schemas.token import TokenPairSchema, TokenSchema, AccessTokenSchema, RefreshTokenSchema, TokenPayloadSchema
from ...settings import settings


def validate_token(token: str) -> TokenPayloadSchema | HTTPException:
    """
    Валидирует содержимое jwt токена, проверяет, не истек ли срок действия токена
    :param token: закодированный jwt токен
    :return: содержимое jwt токена, либо HTTPException, если валидация не прошла или токен просрочен
    """
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
        return TokenPayloadSchema.model_validate(payload)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token not valid')


class AuthorizationToken(HTTPBearer):
    """
    Используется для проверки и валидации токена в заголовке Authorization запросов

    Применение
    __________
    Создайте объект класса и используйте этот объект в качестве зависимости в Depends().

    Результатом создания зависимости будет объект TokenPayloadSchema с содержимым jwt токена.

    Пример
    ______
    def get_current_user(token_data: TokenPayloadSchema = Depends(AuthorizationToken()):
        ...
    """
    def __init__(self, auto_error: bool = True):
        super(AuthorizationToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> TokenPayloadSchema | HTTPException:
        """
        Проверяет наличие и валидирует токен в заголовке Authorization запросов.
        :param request: запрос
        :return: содержимое токена, либо HTTPException, если токена нет или валидация не прошла
        """
        credentials: HTTPAuthorizationCredentials = await super(AuthorizationToken, self).__call__(request)
        token_payload = validate_token(credentials.credentials)
        return token_payload


class TokenPairService:
    """
    Используется для генерации и обновления пары access и refresh токенов
    """
    def __init__(self, auth_service: AuthService = Depends(AuthService)):
        self.auth_service = auth_service

    def refresh_token_pair(self, refresh_token: str) -> TokenPairSchema:
        """
        Обновляет и возвращает пару refresh и access токенов для пользователя
        :param refresh_token: закодированный refresh токен
        :return: новая пара access и refresh токенов для пользователя
        """
        token_data: TokenPayloadSchema = validate_token(refresh_token)
        if token_data.user_role == "operator":
            user: Operator = self.auth_service.get_operator_by_id(token_data.user_id)
        else:
            user: Client = self.auth_service.get_client_by_id(token_data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Пользователь не найден')
        return self.generate_token_pair(user)

    def generate_token_pair(self, user: Operator | Client) -> TokenPairSchema:
        """
         Генерирует и возвращает пару refresh и access токенов для пользователя
        :param user: модель оператора или клиента, для которого генерируется токен
        :return: пара access и refresh токенов для указанного пользователя
        """
        if isinstance(user, Operator):
            user_data = OperatorSchema.model_validate(user)
        else:
            user_data = ClientSchema.model_validate(user)
        access_token: str = self.generate_token(user_data, token_schema=AccessTokenSchema())
        refresh_token: str = self.generate_token(user_data, token_schema=RefreshTokenSchema())
        return TokenPairSchema(user=user_data, access_token=access_token, refresh_token=refresh_token)

    def generate_token(self, user_data: OperatorSchema | ClientSchema, token_schema: TokenSchema) -> str:
        """
        Генерирует и возвращает jwt токен в зависимости от типа пользователя и токена
        :param user_data: pydantic модель оператора или клиента, для которого генерируется токен
        :param token_schema: схема токена со сроком истечения действия и типом токена
        :return: закодированный jwt токен
        """
        payload: TokenPayloadSchema = self.generate_payload(user_data, token_schema)
        token: str = jwt.encode(
            payload.model_dump(),
            key=base64.b64decode(settings.jwt_secret).decode('utf-8'),
            algorithm=settings.jwt_algorithm,
        )
        return token

    @classmethod
    def generate_payload(cls, user_data: OperatorSchema | ClientSchema, token_schema: TokenSchema) \
            -> TokenPayloadSchema:
        """
        Генерирует и возвращает содержимое, которое будет зашито в jwt токен
        в зависимости от типа пользователя и токена
        :param user_data: pydantic модель оператора или клиента, для которого генерируется токен
        :param token_schema: схема токена со сроком истечения действия и типом токена
        :return:  содержимое (payload) jwt токена
        """
        now: datetime = datetime.now(timezone.utc)
        payload: TokenPayloadSchema = TokenPayloadSchema(
            token_type=token_schema.token_type,
            iat=now,
            exp=now + timedelta(minutes=token_schema.expires_in),
            user_id=user_data.id,
            user_role=user_data.role
        )
        return payload



