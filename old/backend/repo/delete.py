from pydantic import BaseModel
from sqlalchemy.orm import Session

from tables import Base

from .base import BaseRepo


class DeleteRepo[TableType: Base, ReadModel: BaseModel](BaseRepo[TableType, ReadModel]):

    def delete_record(self, id: int, session: Session) -> TableType:
        record: TableType | None = (
            session.query(self.table_class)
            .filter(
                self.table_class.id == id,
                self.table_class.is_deleted == False,
            )
            .one_or_none()
        )

        if record is None:
            raise ValueError("Record not found")

        record.is_deleted = True
        session.commit()
        session.refresh(record)
        return record

    def delete(self, id: int, session: Session) -> ReadModel:
        record = self.delete_record(id, session)
        return self.to_read_model(record)
