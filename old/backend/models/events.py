from datetime import date
from models.base import RepoBaseModel, RepoBaseIdModel

class CreateEventModel(RepoBaseModel):
    region_id: int
    event_date: date
    type: str
    severity: int | None = None
    description: str | None = None
    economic_loss: float | None = None

class EventModel(CreateEventModel, RepoBaseIdModel):
    pass

class UpdateEventModel(RepoBaseIdModel):
    region_id: int | None = None
    event_date: date | None = None
    type: str | None = None
    severity: int | None = None
    description: str | None = None
    economic_loss: float | None = None