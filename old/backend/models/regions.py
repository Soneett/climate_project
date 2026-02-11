from models.base import RepoBaseModel, RepoBaseIdModel

class CreateRegionModel(RepoBaseModel):
    name: str
    code: str | None = None
    type: str
    parent_id: int | None = None

class RegionModel(CreateRegionModel, RepoBaseIdModel):
    pass

class UpdateRegionModel(RepoBaseIdModel):
    name: str | None = None
    code: str | None = None
    type: str | None = None
    parent_id: int | None = None