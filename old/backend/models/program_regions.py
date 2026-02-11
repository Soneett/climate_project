from models.base import RepoBaseModel, RepoBaseIdModel

class CreateProgramRegionModel(RepoBaseModel):
    program_id: int
    region_id: int

class ProgramRegionModel(CreateProgramRegionModel, RepoBaseIdModel):
    pass

class UpdateProgramRegionModel(RepoBaseIdModel):
    program_id: int | None = None
    region_id: int | None = None