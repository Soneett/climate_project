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
    legendLeftItems: list[str] = []
    legendRightItems: list[str] = []
    timelineData: list[PieTimelinePointModel]


class WaffleChartTimelineSeriesItemModel(BaseModel):
    name: str
    value: float
    absoluteValue: float


class WaffleChartTimelinePointModel(BaseModel):
    data: list[WaffleChartTimelineSeriesItemModel]


class WaffleChartResponseModel(BaseModel):
    timelineLabels: list[str]
    timelineData: list[WaffleChartTimelinePointModel]


class StackPlotSeriesItemModel(BaseModel):
    name: str
    data: list[float]


class StackPlotResponseModel(BaseModel):
    timelineLabels: list[str]
    legendItems: list[str]
    seriesData: list[StackPlotSeriesItemModel]


class PopulationPyramidTimelinePointModel(BaseModel):
    title: dict[str, str]
    series: list[dict[str, list[float]]]


class PopulationPyramidResponseModel(BaseModel):
    categories: list[str]
    legendItems: list[str]
    timelineLabels: list[str]
    timelineData: list[PopulationPyramidTimelinePointModel]
