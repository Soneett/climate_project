from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from models import IndicatorValueModel, CreateIndicatorValueModel, UpdateIndicatorValueModel, QueryParamsModel
from tables.indicator_values import IndicatorValuesTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/indicator_values", tags=["Indicator Values"])

IndicatorValueRepo = CRUDRepo[IndicatorValuesTable, IndicatorValueModel, CreateIndicatorValueModel, UpdateIndicatorValueModel]

def get_repo() -> IndicatorValueRepo:
    return CRUDRepo(IndicatorValuesTable, IndicatorValueModel, CreateIndicatorValueModel, UpdateIndicatorValueModel)

@router.get("/get", response_model=IndicatorValueModel)
async def get_indicator_value(
    id: int,
    session: Session = Depends(get_db),
    repo: IndicatorValueRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[IndicatorValueModel])
async def get_indicator_values(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    session: Session = Depends(get_db),
    repo: IndicatorValueRepo = Depends(get_repo),
):
    params = QueryParamsModel(limit=limit, offset=offset)
    return repo.get_chunk(session, params)

@router.get("/get_count", response_model=int)
async def get_indicator_values_count(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    session: Session = Depends(get_db),
    repo: IndicatorValueRepo = Depends(get_repo),
):
    params = QueryParamsModel(limit=limit, offset=offset)
    return repo.get_count(session, params)

@router.post("/create", response_model=IndicatorValueModel)
async def create_indicator_value(
    item: CreateIndicatorValueModel,
    session: Session = Depends(get_db),
    repo: IndicatorValueRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.post("/bulk_create", response_model=list[IndicatorValueModel])
async def bulk_create_indicator_values(
    items: list[CreateIndicatorValueModel],
    session: Session = Depends(get_db),
    repo: IndicatorValueRepo = Depends(get_repo),
):
    return repo.bulk_create(items, session)

@router.put("/update", response_model=IndicatorValueModel)
async def update_indicator_value(
    item: UpdateIndicatorValueModel,
    session: Session = Depends(get_db),
    repo: IndicatorValueRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=IndicatorValueModel)
async def delete_indicator_value(
    id: int,
    session: Session = Depends(get_db),
    repo: IndicatorValueRepo = Depends(get_repo),
):
    return repo.delete(id, session)