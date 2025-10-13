from pydantic import BaseModel, ConfigDict


class RepoBaseModel(BaseModel):
    model_config = ConfigDict(extra='ignore')


class RepoBaseIdModel(RepoBaseModel):
    id: int
