from typing import Any
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import BigInteger


from .camel_snake import CamelToSnake


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        BigInteger, name="id", primary_key=True, autoincrement=True
    )

    @declared_attr
    def __tablename__(cls):
        """
        Generate table name from class name:
        OrbitsTable -> orbits
        PoincareSectionsTable -> poincare_sections
        """
        return CamelToSnake.convert(cls.__name__.replace("Table", ""))

    def to_dict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def update_from_dict(self, data: dict[str, Any]):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def eager_to_dict(self, *userels: str, only_ids: bool = False) -> dict[str, Any]:
        data = self.to_dict()
        relationships = inspect(self.__class__).relationships

        if userels:
            rel_names = [rel.key for rel in relationships if rel.key in userels]
        else:
            rel_names = [rel.key for rel in relationships]

        for rel_name in rel_names:
            value = getattr(self, rel_name)
            if isinstance(value, list):
                data[rel_name] = [
                    item.id if only_ids else item.to_dict() for item in value
                ]
            elif value is None:
                data[rel_name] = None
            else:
                data[rel_name] = value.id if only_ids else value.to_dict()
        return data
