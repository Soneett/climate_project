from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from tables.base import Base

class ProgramRegionsTable(Base):
    program_id: Mapped[int] = mapped_column(ForeignKey("regional_programs.id"))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    
    __table_args__ = (
        UniqueConstraint('program_id', 'region_id', name='uq_program_region'),
    )
