from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from models import PopulationAgeSexModel, CreatePopulationAgeSexModel, UpdatePopulationAgeSexModel, QueryParamsModel
from tables.population_age_sex import PopulationAgeSexTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/population", tags=["Population Age/Sex"])

PopulationRepo = CRUDRepo[PopulationAgeSexTable, PopulationAgeSexModel, CreatePopulationAgeSexModel, UpdatePopulationAgeSexModel]

def get_repo() -> PopulationRepo:
    return CRUDRepo(PopulationAgeSexTable, PopulationAgeSexModel, CreatePopulationAgeSexModel, UpdatePopulationAgeSexModel)

@router.get("/get", response_model=PopulationAgeSexModel)
async def get_population_data(
    id: int,
    session: Session = Depends(get_db),
    repo: PopulationRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[PopulationAgeSexModel])
async def get_population_data_chunk(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: PopulationRepo = Depends(get_repo),
):
    return repo.get_chunk(session, params)

@router.get("/get_count", response_model=int)
async def get_indicator_values_count(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(get_db),
    repo: PopulationRepo = Depends(get_repo),
):
    return repo.get_count(session, params)

@router.post("/create", response_model=PopulationAgeSexModel)
async def create_population_data(
    item: CreatePopulationAgeSexModel,
    session: Session = Depends(get_db),
    repo: PopulationRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.post("/bulk_create", response_model=list[PopulationAgeSexModel])
async def bulk_create_population_data(
    items: list[CreatePopulationAgeSexModel],
    session: Session = Depends(get_db),
    repo: PopulationRepo = Depends(get_repo),
):
    return repo.bulk_create(items, session)

@router.put("/update", response_model=PopulationAgeSexModel)
async def update_population_data(
    item: UpdatePopulationAgeSexModel,
    session: Session = Depends(get_db),
    repo: PopulationRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=PopulationAgeSexModel)
async def delete_population_data(
    id: int,
    session: Session = Depends(get_db),
    repo: PopulationRepo = Depends(get_repo),
):
    return repo.delete(id, session)