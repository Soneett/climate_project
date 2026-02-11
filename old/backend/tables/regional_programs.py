from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float
from typing import List, Optional

from tables.base import Base

class RegionalProgramsTable(Base):
    name: Mapped[str]
    level: Mapped[str]  
    start_year: Mapped[int]
    end_year: Mapped[Optional[int]]  
    description: Mapped[Optional[str]]
    status: Mapped[str]
    budget_total: Mapped[Optional[float]]
    

 