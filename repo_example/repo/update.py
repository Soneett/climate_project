from typing import Type

from sqlalchemy.orm import Session

from models import RepoBaseModel, RepoBaseIdModel
from tables import Base

from .base import BaseRepo


class UpdateRepo[TableType: Base, ReadModel: RepoBaseModel, UpdateModel: RepoBaseIdModel](
    BaseRepo[TableType, ReadModel]
):
    def __init__(
        self,
        table_class: Type[TableType],
        read_model_class: Type[ReadModel],
        update_model_class: Type[UpdateModel],
    ):
        BaseRepo.__init__(self, table_class, read_model_class)
        self.update_model_class = update_model_class

    def update_return_record(self, item: UpdateModel, session: Session) -> TableType:
        record: TableType = session.get(self.table_class, item.id)
        item_dict = item.model_dump(exclude_none=True)
        record.update_from_dict(item_dict)
        session.commit()
        # session.refresh(record)
        return record

    def update(self, item: UpdateModel, session: Session) -> ReadModel:
        record = self.update_return_record(item, session)
        return self.to_read_model(record)
