from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, Float
from typing import Optional
from datetime import date

from tables.base import Base

class EventsTable(Base):
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    event_date: Mapped[date] 
    type: Mapped[str]  
    severity: Mapped[Optional[int]]  
    description: Mapped[Optional[str]]
    economic_loss: Mapped[Optional[float]] 
    