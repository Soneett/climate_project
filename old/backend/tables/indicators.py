from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional

from tables.base import Base

class IndicatorsTable(Base):

    name: Mapped[str]
    unit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("units.id"))
    type: Mapped[str]
    theme: Mapped[str]
    subtype_id: Mapped[Optional[int]] = mapped_column(ForeignKey("indicator_subtypes.id"))