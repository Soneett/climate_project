from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from models import UnitModel, CreateUnitModel, UpdateUnitModel, QueryParamsModel
from tables.units import UnitsTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/units", tags=["Units"])

UnitRepo = CRUDRepo[UnitsTable, UnitModel, CreateUnitModel, UpdateUnitModel]

def get_repo() -> UnitRepo:
    return CRUDRepo(UnitsTable, UnitModel, CreateUnitModel, UpdateUnitModel)

@router.get("/get", response_model=UnitModel)
async def get_unit(
    id: int,
    session: Session = Depends(get_db),
    repo: UnitRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[UnitModel])
async def get_units(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: UnitRepo = Depends(get_repo),
):
    return repo.get_chunk(session, params)

@router.get("/get_count", response_model=int)
async def get_units_count(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: UnitRepo = Depends(get_repo),
):
    return repo.get_count(session, params)

@router.post("/create", response_model=UnitModel)
async def create_unit(
    item: CreateUnitModel,
    session: Session = Depends(get_db),
    repo: UnitRepo = Depends(get_repo),
):
    return repo.create(item, session)
