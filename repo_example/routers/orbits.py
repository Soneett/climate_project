from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from models import (
    OrbitModel,
    CreateOrbitModel,
    UpdateOrbitModel,
    QueryParamsModel,
)
from tables import OrbitsTable
from repo import CRUDRepo
from database import db

orbits_router = APIRouter(prefix="/orbits", tags=["Orbits"])

RepoClass = CRUDRepo[OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel]


def create_repo() -> RepoClass:
    return RepoClass(OrbitsTable, OrbitModel, CreateOrbitModel, UpdateOrbitModel)


@orbits_router.get("/get", response_model=OrbitModel)
async def get(
    id: int,
    session: Session = Depends(db.create_session),
    repo: RepoClass = Depends(create_repo),
):
    return repo.get(id, session)


@orbits_router.get("/get_chunk", response_model=list[OrbitModel])
async def get_chunk(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(db.create_session),
    repo: RepoClass = Depends(create_repo),
):
    return repo.get_chunk(session, params)


@orbits_router.get("/get_count", response_model=int)
async def get_count(
    params: QueryParamsModel = Body(default=None),
    session: Session = Depends(db.create_session),
    repo: RepoClass = Depends(create_repo),
):
    return repo.get_count(session, params)


@orbits_router.post("/create", response_model=OrbitModel)
async def create(
    item: CreateOrbitModel,
    session: Session = Depends(db.create_session),
    repo: RepoClass = Depends(create_repo),
):
    return repo.create(item, session)


@orbits_router.post("/bulk_create", response_model=OrbitModel)
async def bulk_create(
    items: list[CreateOrbitModel],
    session: Session = Depends(db.create_session),
    repo: RepoClass = Depends(create_repo),
):
    return repo.bulk_create(items, session)


@orbits_router.put("/update", response_model=OrbitModel)
async def update(
    item: UpdateOrbitModel,
    session: Session = Depends(db.create_session),
    repo: RepoClass = Depends(create_repo),
):
    return repo.update(item, session)


@orbits_router.delete("/delete", response_model=OrbitModel)
async def delete(
    id: int,
    session: Session = Depends(db.create_session),
    repo: RepoClass = Depends(create_repo),
):
    return repo.delete(id, session)
