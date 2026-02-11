from models.base import RepoBaseModel, RepoBaseIdModel
'''
Хранит числовые значения показателей для разных регионов и лет.

id - уникальный номер записи
indicator_id - ссылка на показатель (indicators.id)
region_id - ссылка на регион (regions.id)
year - год, к которому относится показатель
value - числовое значение (например, 6,5 (%))
source_id - ссылка на источник данных (data_sources.id)
'''

class CreateIndicatorValueModel(RepoBaseModel):
    indicator_id: int
    region_id: int
    source_id: int
    year: int
    value: float

class IndicatorValueModel(CreateIndicatorValueModel, RepoBaseIdModel):
    pass

class UpdateIndicatorValueModel(RepoBaseIdModel):
    indicator_id: int | None = None
    region_id: int | None = None
    source_id: int | None = None
    year: int | None = None
    value: float | None = None

