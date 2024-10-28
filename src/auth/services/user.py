from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from .. import utils
from ..services.token import AuthorizationToken
from ...database import database as db
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
    if token_data.user_role == "operator":
        user: Operator = session.query(Operator).get(token_data.user_id)
    else:
        user: Client = session.query(Client).get(token_data.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Пользователь не найден')
    if isinstance(user, Operator):
        return utils.create_operator_data(user)
    return utils.create_client_data(user, token_data.user_login_number)
