from datetime import date
from models.base import RepoBaseModel, RepoBaseIdModel

class CreateRegionalProgramModel(RepoBaseModel):
    name: str
    level: str
    start_year: int
    end_year: int | None = None
    description: str | None = None
    status: str
    budget_total: float | None = None

class RegionalProgramModel(CreateRegionalProgramModel, RepoBaseIdModel):
    pass

class UpdateRegionalProgramModel(RepoBaseIdModel):
    name: str | None = None
    level: str | None = None
    start_year: int | None = None
    end_year: int | None = None
    description: str | None = None
    status: str | None = None
    budget_total: float | None = None