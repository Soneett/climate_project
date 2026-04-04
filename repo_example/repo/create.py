from typing import Type

from pydantic import BaseModel
from sqlalchemy.orm import Session

from tables import Base

from .base import BaseRepo


class CreateRepo[TableType: Base, ReadModel: BaseModel, CreateModel: BaseModel](
    BaseRepo[TableType, ReadModel]
):
    def __init__(
        self,
        table_class: Type[TableType],
        read_model_class: Type[ReadModel],
        create_model_class: Type[CreateModel],
    ):
        BaseRepo.__init__(self, table_class, read_model_class)
        self.create_model_class = create_model_class

    def from_create_model(self, item: CreateModel) -> TableType:
        item_dict = item.model_dump()
        record = self.table_class(**item_dict)
        return record

    def create_record(self, item: CreateModel, session: Session) -> TableType:
        record = self.from_create_model(item)
        session.add(record)
        session.commit()
        # session.refresh(record)
        return record

    def create(self, item: CreateModel, session: Session) -> ReadModel:
        record = self.create_record(item, session)
        return self.to_read_model(record)

    def bulk_create_records(
        self, items: list[CreateModel], session: Session
    ) -> list[TableType]:
        records = [self.from_create_model(item) for item in items]
        session.bulk_save_objects(records, return_defaults=True)
        session.commit()
        return records

    def bulk_create(
        self, items: list[CreateModel], session: Session
    ) -> list[ReadModel]:
        records = self.bulk_create_records(items, session)
        return self.to_read_model_list(records)
