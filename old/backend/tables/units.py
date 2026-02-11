from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from tables.base import Base

class UnitsTable(Base):
    code: Mapped[str]
    name: Mapped[str]
