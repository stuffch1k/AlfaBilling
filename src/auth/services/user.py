import json

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from ..services.token import AuthorizationToken
from ...database import database as db, redis_db
from ..schemas.client import ClientSchema
from ..schemas.models import Operator, Client
from ..schemas.operator import OperatorSchema
from ..schemas.token import TokenPayloadSchema


def get_current_user(token_data: TokenPayloadSchema = Depends(AuthorizationToken()),
                     session: Session = Depends(db.get_session)) -> OperatorSchema | ClientSchema:
    """
    Возвращает модель текущего аутентифицированного пользователя

    Применение
    __________
    Используйте эту функцию в качестве зависимости в Depends().

    Результатом создания зависимости будет объект OperatorSchema или ClientSchema с инф-ей о пользователе

    Пример
    ______
        @user_router.get('/user')
    def get_current_user(user: OperatorSchema | ClientSchema = Depends(get_current_user)) \
        -> OperatorSchema | ClientSchema:
    return user

    :param token_data: содержимое jwt токена из заголовка Authorization запроса
    :param session: сессия для подключения к бд
    :return: Модель оператора или клиента в зависимости от роли, зашитой в токене
    """
    cached_user = get_cached_user_schema(token_data)
    if cached_user:
        return cached_user
    user_from_db_schema = get_db_user_schema(token_data, session)
    set_user_to_cache(user_from_db_schema)
    return user_from_db_schema


def get_db_user_schema(token_data: TokenPayloadSchema,
                       session: Session) -> OperatorSchema | ClientSchema:
    try:
        if token_data.user_role == "operator":
            user: Operator = session.query(Operator).get(token_data.user_id)
            user_schema = user.create_schema()
        else:
            user: Client = session.query(Client).get(token_data.user_id)
            user_schema = user.create_schema(number=token_data.user_login_number)
        return user_schema
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь не найден")


def get_cached_user_schema(token_data: TokenPayloadSchema) -> ClientSchema | OperatorSchema:
    try:
        if token_data.user_role == "operator":
            return get_cached_operator_schema(token_data)
        return get_cached_client_schema(token_data)
    except Exception:
        return None


def get_cached_operator_schema(token_data: TokenPayloadSchema) -> OperatorSchema | None:
    cache_key = f"users:operator:{token_data.user_id}"
    cached_operator: str = redis_db.get(cache_key)
    if cached_operator:
        return OperatorSchema.model_validate(json.loads(cached_operator))
    return None


def get_cached_client_schema(token_data: TokenPayloadSchema) -> ClientSchema | None:
    cache_key = f"users:client:{token_data.user_id}"
    cached_client: str = redis_db.get(cache_key)
    if cached_client:
        return ClientSchema.model_validate(json.loads(cached_client))
    return None


def set_user_to_cache(user_schema: ClientSchema | OperatorSchema):
    if isinstance(user_schema, OperatorSchema):
        cache_key = f"users:operator:{user_schema.id}"
    else:
        cache_key = f"users:client:{user_schema.id}"
    try:
        redis_db.set(name=cache_key, value=user_schema.model_dump_json())
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error caching data: {e}")