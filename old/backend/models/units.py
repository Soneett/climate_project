from models.base import RepoBaseModel, RepoBaseIdModel

class CreateUnitModel(RepoBaseModel):
    code: str
    name: str

class UnitModel(CreateUnitModel, RepoBaseIdModel):
    pass

class UpdateUnitModel(RepoBaseIdModel):
    code: str | None = None
    name: str | None = None