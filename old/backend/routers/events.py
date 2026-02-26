from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from models import EventModel, CreateEventModel, UpdateEventModel, QueryParamsModel
from tables.events import EventsTable
from repo import CRUDRepo
from database import get_db

router = APIRouter(prefix="/events", tags=["Events"])

EventRepo = CRUDRepo[EventsTable, EventModel, CreateEventModel, UpdateEventModel]

def get_repo() -> EventRepo:
    return CRUDRepo(EventsTable, EventModel, CreateEventModel, UpdateEventModel)

@router.get("/get", response_model=EventModel)
async def get_event(
    id: int,
    session: Session = Depends(get_db),
    repo: EventRepo = Depends(get_repo),
):
    return repo.get(id, session)

@router.get("/get_chunk", response_model=list[EventModel])
async def get_events(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    session: Session = Depends(get_db),
    repo: EventRepo = Depends(get_repo),
):
    params = QueryParamsModel(limit=limit, offset=offset)
    return repo.get_chunk(session, params)

@router.get("/get_count", response_model=int)
async def get_events_count(
    limit: int | None = Query(None, ge=0),
    offset: int | None = Query(None, ge=0),
    session: Session = Depends(get_db),
    repo: EventRepo = Depends(get_repo),
):
    params = QueryParamsModel(limit=limit, offset=offset)
    return repo.get_count(session, params)

@router.post("/create", response_model=EventModel)
async def create_event(
    item: CreateEventModel,
    session: Session = Depends(get_db),
    repo: EventRepo = Depends(get_repo),
):
    return repo.create(item, session)

@router.put("/update", response_model=EventModel)
async def update_event(
    item: UpdateEventModel,
    session: Session = Depends(get_db),
    repo: EventRepo = Depends(get_repo),
):
    return repo.update(item, session)

@router.delete("/delete", response_model=EventModel)
async def delete_event(
    id: int,
    session: Session = Depends(get_db),
    repo: EventRepo = Depends(get_repo),
):
    return repo.delete(id, session)