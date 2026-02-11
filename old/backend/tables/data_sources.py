from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date
from typing import Optional
from datetime import date

from tables.base import Base

class DataSourcesTable(Base):
    name: Mapped[str]
    url: Mapped[Optional[str]]
    organization: Mapped[Optional[str]]
    date_collected: Mapped[Optional[date]]