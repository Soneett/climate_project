from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from models import RegionalProgramModel, CreateRegionalProgramModel, UpdateRegionalProgramModel, QueryParamsModel
from tables.regional_programs import RegionalProgramsTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/programs", tags=["Regional Programs"])

RegionalProgramRepo = CRUDRepo[RegionalProgramsTable, RegionalProgramModel, CreateRegionalProgramModel, UpdateRegionalProgramModel]

def get_repo() -> RegionalProgramRepo:
    return CRUDRepo(RegionalProgramsTable, RegionalProgramModel, CreateRegionalProgramModel, UpdateRegionalProgramModel)

@router.get("/get", response_model=RegionalProgramModel)
async def get_program(
    id: int,
    session: Session = Depends(get_db),
    repo: RegionalProgramRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[RegionalProgramModel])
async def get_programs(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: RegionalProgramRepo = Depends(get_repo),
):
    return repo.get_chunk(session, params)

@router.post("/create", response_model=RegionalProgramModel)
async def create_program(
    item: CreateRegionalProgramModel,
    session: Session = Depends(get_db),
    repo: RegionalProgramRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.put("/update", response_model=RegionalProgramModel)
async def update_program(
    item: UpdateRegionalProgramModel,
    session: Session = Depends(get_db),
    repo: RegionalProgramRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=RegionalProgramModel)
async def delete_program(
    id: int,
    session: Session = Depends(get_db),
    repo: RegionalProgramRepo = Depends(get_repo),
):
    return repo.delete(id, session)