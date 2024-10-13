from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from ..schemas.token import TokenPairSchema
from ..services.token import TokenPairService

token_router = APIRouter(prefix='/jwt')


@token_router.get('/logout')
def logout(response: Response) -> dict:
    response.delete_cookie(key='refresh_token')
    return {"detail": "Successfully logged out"}


@token_router.get('/refresh')
def refresh(request: Request,
            response: Response,
            token_service: TokenPairService = Depends()) -> dict:
    refresh_token: str = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Пользователь не авторизован")
    new_token_pair: TokenPairSchema = token_service.refresh_token_pair(refresh_token)
    response.set_cookie(key='refresh_token', value=new_token_pair.refresh_token,
                        max_age=3 * 24 * 60 * 60, httponly=True)
    return {"access_token": new_token_pair.access_token}
