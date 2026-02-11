from models.base import RepoBaseModel, RepoBaseIdModel

class CreatePopulationAgeSexModel(RepoBaseModel):
    region_id: int
    year: int
    age_code: str
    sex_code: str
    value: int
    source_id: int

class PopulationAgeSexModel(CreatePopulationAgeSexModel, RepoBaseIdModel):
    pass

class UpdatePopulationAgeSexModel(RepoBaseIdModel):
    region_id: int | None = None
    year: int | None = None
    age_code: str | None = None
    sex_code: str | None = None
    value: int | None = None
    source_id: int | None = None