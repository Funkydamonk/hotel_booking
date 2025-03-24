from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=None, description="Page", ge=1)]
    per_page: Annotated[int | None, Query(default=None, description="Items per page", ge=1, le=100)]


PaginationDep = Annotated[PaginationParams, Depends()]
