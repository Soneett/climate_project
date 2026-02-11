from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from models import IndicatorSubtypeModel, CreateIndicatorSubtypeModel, UpdateIndicatorSubtypeModel, QueryParamsModel
from tables.indicator_subtypes import IndicatorSubtypesTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/indicator_subtypes", tags=["Indicator Subtypes"])

IndicatorSubtypeRepo = CRUDRepo[IndicatorSubtypesTable, IndicatorSubtypeModel, CreateIndicatorSubtypeModel, UpdateIndicatorSubtypeModel]

def get_repo() -> IndicatorSubtypeRepo:
    return CRUDRepo(IndicatorSubtypesTable, IndicatorSubtypeModel, CreateIndicatorSubtypeModel, UpdateIndicatorSubtypeModel)

@router.get("/get", response_model=IndicatorSubtypeModel)
async def get_indicator_subtype(
    id: int,
    session: Session = Depends(get_db),
    repo: IndicatorSubtypeRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[IndicatorSubtypeModel])
async def get_indicator_subtypes(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: IndicatorSubtypeRepo = Depends(get_repo),
):
    return repo.get_chunk(session, params)

@router.post("/create", response_model=IndicatorSubtypeModel)
async def create_indicator_subtype(
    item: CreateIndicatorSubtypeModel,
    session: Session = Depends(get_db),
    repo: IndicatorSubtypeRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.put("/update", response_model=IndicatorSubtypeModel)
async def update_indicator_subtype(
    item: UpdateIndicatorSubtypeModel,
    session: Session = Depends(get_db),
    repo: IndicatorSubtypeRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=IndicatorSubtypeModel)
async def delete_indicator_subtype(
    id: int,
    session: Session = Depends(get_db),
    repo: IndicatorSubtypeRepo = Depends(get_repo),
):
    return repo.delete(id, session)