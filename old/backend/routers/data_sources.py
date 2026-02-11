from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from models import DataSourceModel, CreateDataSourceModel, UpdateDataSourceModel, QueryParamsModel
from tables.data_sources import DataSourcesTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/data_sources", tags=["Data Sources"])

DataSourceRepo = CRUDRepo[DataSourcesTable, DataSourceModel, CreateDataSourceModel, UpdateDataSourceModel]

def get_repo() -> DataSourceRepo:
    return CRUDRepo(DataSourcesTable, DataSourceModel, CreateDataSourceModel, UpdateDataSourceModel)

@router.get("/get", response_model=DataSourceModel)
async def get_data_source(
    id: int,
    session: Session = Depends(get_db),
    repo: DataSourceRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[DataSourceModel])
async def get_data_sources(
    params: QueryParamsModel = Depends(),
    session: Session = Depends(get_db),
    repo: DataSourceRepo = Depends(get_repo),
):
    return repo.get_chunk(session, params)

@router.post("/create", response_model=DataSourceModel)
async def create_data_source(
    item: CreateDataSourceModel,
    session: Session = Depends(get_db),
    repo: DataSourceRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.put("/update", response_model=DataSourceModel)
async def update_data_source(
    item: UpdateDataSourceModel,
    session: Session = Depends(get_db),
    repo: DataSourceRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=DataSourceModel)
async def delete_data_source(
    id: int,
    session: Session = Depends(get_db),
    repo: DataSourceRepo = Depends(get_repo),
):
    return repo.delete(id, session)