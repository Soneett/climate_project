from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from tables.base import Base

class IndicatorSubtypesTable(Base):
    name: Mapped[str]
    