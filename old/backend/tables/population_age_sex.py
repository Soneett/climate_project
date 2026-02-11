from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer
from tables.base import Base

class PopulationAgeSexTable(Base):

    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    year: Mapped[int]
    age_code: Mapped[str] 
    sex_code: Mapped[str] 
    value: Mapped[int] 
    source_id: Mapped[int] = mapped_column(ForeignKey("data_sources.id"))
    
