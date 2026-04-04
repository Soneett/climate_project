from pydantic import BaseModel
from sqlalchemy.orm import Session

from tables import Base

from .base import BaseRepo


class DeleteRepo[TableType: Base, ReadModel: BaseModel](BaseRepo[TableType, ReadModel]):

    def delete_record(self, id: int, session: Session) -> TableType:
        record = session.get(self.table_class, id)
        session.delete(record)
        session.commit()
        return record

    def delete(self, id: int, session: Session) -> ReadModel:
        record = self.delete_record(id, session)
        return self.to_read_model(record)
