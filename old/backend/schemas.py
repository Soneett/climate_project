from pydantic import BaseModel

class IndicatorBase(BaseModel):
    name: str
    type: str
    unit: str

class IndicatorOut(BaseModel):
    id: int
    name: str
    type: str
    unit: str

    class Config:
        orm_mode = True
