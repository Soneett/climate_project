from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from models import IndicatorModel, CreateIndicatorModel, UpdateIndicatorModel, QueryParamsModel
from tables.indicators import IndicatorsTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/indicators", tags=["Indicators"])

IndicatorRepo = CRUDRepo[IndicatorsTable, IndicatorModel, CreateIndicatorModel, UpdateIndicatorModel]

def get_repo() -> IndicatorRepo:
    return CRUDRepo(IndicatorsTable, IndicatorModel, CreateIndicatorModel, UpdateIndicatorModel)

@router.get("/get", response_model=IndicatorModel)
async def get_indicator(
    id: int,
    session: Session = Depends(get_db),
    repo: IndicatorRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[IndicatorModel])
async def get_indicators(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: IndicatorRepo = Depends(get_repo),
):
    return repo.get_chunk(session, params)

@router.get("/get_count", response_model=int)
async def get_indicators_count(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: IndicatorRepo = Depends(get_repo),
):
    return repo.get_count(session, params)

@router.post("/create", response_model=IndicatorModel)
async def create_indicator(
    item: CreateIndicatorModel,
    session: Session = Depends(get_db),
    repo: IndicatorRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.post("/bulk_create", response_model=list[IndicatorModel])
async def bulk_create_indicators(
    items: list[CreateIndicatorModel],
    session: Session = Depends(get_db),
    repo: IndicatorRepo = Depends(get_repo),
):
    return repo.bulk_create(items, session)

@router.put("/update", response_model=IndicatorModel)
async def update_indicator(
    item: UpdateIndicatorModel,
    session: Session = Depends(get_db),
    repo: IndicatorRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=IndicatorModel)
async def delete_indicator(
    id: int,
    session: Session = Depends(get_db),
    repo: IndicatorRepo = Depends(get_repo),
):
    return repo.delete(id, session)