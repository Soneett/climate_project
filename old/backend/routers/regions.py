from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from models import RegionModel, CreateRegionModel, UpdateRegionModel, QueryParamsModel
from tables.regions import RegionsTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/regions", tags=["Regions"])

RegionRepo = CRUDRepo[RegionsTable, RegionModel, CreateRegionModel, UpdateRegionModel]

def get_repo() -> RegionRepo:
    return CRUDRepo(RegionsTable, RegionModel, CreateRegionModel, UpdateRegionModel)

@router.get("/get", response_model=RegionModel)
async def get_region(
    id: int = Query(..., description="ID региона"), 
    session: Session = Depends(get_db),
    repo: RegionRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[RegionModel])
async def get_regions(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    session: Session = Depends(get_db),
    repo: RegionRepo = Depends(get_repo),
):
    params = QueryParamsModel(limit=limit, offset=offset)
    return repo.get_chunk(session, params)

@router.get("/get_count", response_model=int)
async def get_regions_count(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    session: Session = Depends(get_db),
    repo: RegionRepo = Depends(get_repo),
):
    params = QueryParamsModel(limit=limit, offset=offset)
    return repo.get_count(session, params)

@router.post("/create", response_model=RegionModel)
async def create_region(
    item: CreateRegionModel,
    session: Session = Depends(get_db),
    repo: RegionRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.put("/update", response_model=RegionModel)
async def update_region(
    item: UpdateRegionModel,
    session: Session = Depends(get_db),
    repo: RegionRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=RegionModel)
async def delete_region(
    id: int,
    session: Session = Depends(get_db),
    repo: RegionRepo = Depends(get_repo),
):
    return repo.delete(id, session)
