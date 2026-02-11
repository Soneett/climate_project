from models.base import RepoBaseModel, RepoBaseIdModel

'''
Справочник всех показателей, которые собираются и анализируются.

id - уникальный номер показателя
name - название (например, «Смертность», «Рождаемость», «Средняя температура»)
unit_id - ссылка на единицу измерения (units.id)
type - общий тип (например, «демография», «экономика», «экология»)
theme - тематическая группа (например, «рождаемость и смертность»)
subtype_id - ссылка на подтип (indicator_subtypes.id)
'''

class CreateIndicatorModel(RepoBaseModel):
    name: str
    unit_id: int | None = None
    type: str
    theme: str
    subtype_id: int | None = None

class IndicatorModel(CreateIndicatorModel, RepoBaseIdModel):
    pass

class UpdateIndicatorModel(RepoBaseIdModel):
    name: str | None = None
    unit_id: int | None = None
    type: str | None = None
    theme: str | None = None
    subtype_id: int | None = None
