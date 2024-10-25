from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from .schemas.client import ClientSchema
from .schemas.operator import OperatorSchema
from .services.user import get_current_user


class AllowAny:
    """
    Предоставляет доступ к эндпоинтам всем пользователям
    """
    def __call__(self):
        return True


class AllowAnyAuthenticated:
    """
    Предоставляет доступ к эндпоинтам всем аутентифицированным пользователям
    """
    def __call__(self, user: Annotated[OperatorSchema | ClientSchema, Depends(get_current_user)]) \
            -> OperatorSchema | ClientSchema:
        if user and (user.role == "operator" or user.role == "client"):
            return user


class AllowOperator:
    """
       Предоставляет доступ к эндпоинтам только аутентифицированным пользователям с ролью operator
    """
    def __call__(self, user: Annotated[OperatorSchema | ClientSchema, Depends(get_current_user)])\
            -> OperatorSchema | ClientSchema:
        if user.role == "operator":
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions")


class AllowClient:
    """
       Предоставляет доступ к эндпоинтам только аутентифицированным пользователям с ролью client
    """
    def __call__(self, user: Annotated[OperatorSchema | ClientSchema, Depends(get_current_user)])\
            -> OperatorSchema | ClientSchema:
        if user.role == "client":
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions")


class Permissions:
    """
    Используется для управления правами доступа пользователей

    Attributes
    ----------
    allowAnyAuthenticated : AllowAnyAuthenticated
        Предоставляет доступ к эндпоинтам всем аутентифицированным пользователям
    allowOperator : AllowOperator
        Предоставляет доступ к эндпоинтам только аутентифицированным пользователям с ролью operator
    allowClient : AllowClient
        Предоставляет доступ к эндпоинтам только аутентифицированным пользователям с ролью client
    allowAll : AllowAny
        Предоставляет доступ к эндпоинтам всем пользователям
    """
    allowAnyAuthenticated = AllowAnyAuthenticated()
    allowOperator = AllowOperator()
    allowClient = AllowClient()
    allowAll = AllowAny()


permissions = Permissions()
