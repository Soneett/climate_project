from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Float

from tables.base import Base

class IndicatorValuesTable(Base):
    indicator_id: Mapped[int] = mapped_column(ForeignKey("indicators.id"))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    year: Mapped[int]
    value: Mapped[float] 
    source_id: Mapped[int] = mapped_column(ForeignKey("data_sources.id"))