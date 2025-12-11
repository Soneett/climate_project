from typing import Type

from pydantic import BaseModel

from tables import Base


class BaseRepo[TableType: Base, ReadModel: BaseModel]:

    def __init__(self, table_class: Type[TableType], read_model_class: Type[ReadModel]):
        self.table_class = table_class
        self.read_model_class = read_model_class

    def to_read_model(self, record: TableType) -> ReadModel:
        return self.read_model_class.model_validate(record.to_dict())

    def to_read_model_list(self, records: list[TableType]) -> list[ReadModel]:
        return [self.to_read_model(record) for record in records]
