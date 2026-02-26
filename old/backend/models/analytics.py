from pydantic import BaseModel

class ChartPointModel(BaseModel):
    year: int
    value: float

class ChartSeriesModel(BaseModel):
    indicator_id: int
    indicator_name: str
    points: list[ChartPointModel]

class ChartDataResponseModel(BaseModel):
    region_id: int
    region_name: str
    series: list[ChartSeriesModel]


class PopulationPyramidPointModel(BaseModel):
    age_code: str
    male: float
    female: float
    total: float


class PopulationPyramidResponseModel(BaseModel):
    region_id: int
    region_name: str
    year: int
    points: list[PopulationPyramidPointModel]
