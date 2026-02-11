from datetime import date
from models.base import RepoBaseModel, RepoBaseIdModel

class CreateDataSourceModel(RepoBaseModel):
    name: str
    url: str | None = None
    organization: str | None = None
    date_collected: date | None = None

class DataSourceModel(CreateDataSourceModel, RepoBaseIdModel):
    pass

class UpdateDataSourceModel(RepoBaseIdModel):
    name: str | None = None
    url: str | None = None
    organization: str | None = None
    date_collected: date | None = None