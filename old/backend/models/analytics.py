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
    source_id: int
    series: list[ChartSeriesModel]