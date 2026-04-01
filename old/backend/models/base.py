from pydantic import BaseModel, ConfigDict

class RepoBaseModel(BaseModel):
    model_config = ConfigDict(extra='ignore', from_attributes=True)

class RepoBaseIdModel(RepoBaseModel):
    id: int
