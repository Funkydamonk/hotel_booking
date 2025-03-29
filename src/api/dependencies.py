from typing import Annotated
from fastapi import Depends, Query, Request
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Page", ge=1)]

    per_page: Annotated[int | None, Query(default=None, description="Items per page", ge=1, le=100)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail="Не предоставлен токен")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_token(token)
    return data.get('user_id') 


UserIdDep = Annotated[int, Depends(get_current_user_id)]
