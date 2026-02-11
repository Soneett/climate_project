from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from models import ProgramRegionModel, CreateProgramRegionModel, UpdateProgramRegionModel, QueryParamsModel
from tables.program_regions import ProgramRegionsTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/program_regions", tags=["Program Regions Links"])

ProgramRegionRepo = CRUDRepo[ProgramRegionsTable, ProgramRegionModel, CreateProgramRegionModel, UpdateProgramRegionModel]

def get_repo() -> ProgramRegionRepo:
    return CRUDRepo(ProgramRegionsTable, ProgramRegionModel, CreateProgramRegionModel, UpdateProgramRegionModel)

@router.get("/get_chunk", response_model=list[ProgramRegionModel])
async def get_program_region_links(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: ProgramRegionRepo = Depends(get_repo),
):
    return repo.get_chunk(session, params)

@router.post("/create", response_model=ProgramRegionModel)
async def create_program_region_link(
    item: CreateProgramRegionModel,
    session: Session = Depends(get_db),
    repo: ProgramRegionRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.delete("/delete", response_model=ProgramRegionModel)
async def delete_program_region_link(
    id: int,
    session: Session = Depends(get_db),
    repo: ProgramRegionRepo = Depends(get_repo),
):
    return repo.delete(id, session)