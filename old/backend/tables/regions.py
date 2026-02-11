from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List, Optional

from tables.base import Base

class RegionsTable(Base): 
    name: Mapped[str]
    code: Mapped[Optional[str]]
    type: Mapped[str]
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("regions.id"))

