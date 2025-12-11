from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class FilterOpEnum(StrEnum):
    lk = "like"
    eq = "=="
    ne = "!="
    gt = ">"
    lt = "<"
    ge = ">="
    le = "<="


class FilterModel(BaseModel):
    field: str
    op: FilterOpEnum
    value: Any

    def __repr__(self) -> str:
        return f"{self.field} {self.op} {self.value}"


class PaginationModel(BaseModel):
    limit: int | None = None
    offset: int | None = None


class QueryParamsModel(PaginationModel):
    filters: list[FilterModel] = Field(default_factory=list)
