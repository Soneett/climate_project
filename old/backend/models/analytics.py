from pydantic import BaseModel

class LineChartDatasetModel(BaseModel):
    name: str
    data: list[float]


class LineChartResponseModel(BaseModel):
    labels: list[str]
    datasets: list[LineChartDatasetModel]


class PieTimelineSeriesItemModel(BaseModel):
    value: float
    name: str


class PieTimelinePointModel(BaseModel):
    title: dict[str, str]
    series: list[dict[str, list[PieTimelineSeriesItemModel]]]


class PieChartResponseModel(BaseModel):
    timelineLabels: list[str]
    timelineData: list[PieTimelinePointModel]


class PopulationPyramidTimelinePointModel(BaseModel):
    title: dict[str, str]
    series: list[dict[str, list[float]]]


class PopulationPyramidResponseModel(BaseModel):
    categories: list[str]
    legendItems: list[str]
    timelineLabels: list[str]
    timelineData: list[PopulationPyramidTimelinePointModel]
