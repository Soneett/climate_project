from models.base import RepoBaseModel, RepoBaseIdModel

class CreateIndicatorSubtypeModel(RepoBaseModel):
    name: str

class IndicatorSubtypeModel(CreateIndicatorSubtypeModel, RepoBaseIdModel):
    pass

class UpdateIndicatorSubtypeModel(RepoBaseIdModel):
    name: str | None = None