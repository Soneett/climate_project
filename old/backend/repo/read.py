from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, cast, String

from models import QueryParamsModel, RepoBaseIdModel
from models import FilterOpEnum as Op
from tables import Base

from .base import BaseRepo


class ReadRepo[TableType: Base, ReadModel: RepoBaseIdModel](
    BaseRepo[TableType, ReadModel]
):

    def build_query(
        self,
        session: Session,
        params: QueryParamsModel | None = None,
        query: Query | None = None,
        table_class: TableType | None = None,
    ) -> Query:

        if params is None:
            params = QueryParamsModel()

        if table_class is None:
            table_class = self.table_class

        if query is None:
            query = session.query(table_class).filter(
                table_class.is_deleted == False
                )

        filters = []
        for filter_ in params.filters:
            if not hasattr(table_class, filter_.field):
                continue
            column = getattr(table_class, filter_.field)

            match filter_.op:
                case Op.lk:
                    filters.append(cast(column, String).like(f"%{filter_.value}%"))
                case Op.eq:
                    filters.append(column == filter_.value)
                case Op.ne:
                    filters.append(column != filter_.value)
                case Op.ge:
                    filters.append(column >= filter_.value)
                case Op.gt:
                    filters.append(column > filter_.value)
                case Op.le:
                    filters.append(column <= filter_.value)
                case Op.lt:
                    filters.append(column < filter_.value)

        if filters:
            query = query.filter(and_(*filters))

        if params.offset is not None:
            query = query.offset(params.offset)

        if params.limit is not None:
            query = query.limit(params.limit)

        return query

    def get_record(self, id: int, session: Session) -> TableType | None:
        return (
            session.query(self.table_class).filter(
                self.table_class.id == id,
                self.table_class.is_deleted == False,
            ).one_or_none()
        )

    def get(self, id: int, session: Session) -> ReadModel:
        record = self.get_record(id, session)
        return self.to_read_model(record)

    def get_chunk_records(
        self, session: Session, params: QueryParamsModel | None = None
    ) -> list[TableType]:
        query = self.build_query(session, params)
        return query.all()

    def get_chunk(
        self, session: Session, params: QueryParamsModel | None = None
    ) -> list[TableType]:
        records = self.get_chunk_records(session, params)
        return self.to_read_model_list(records)

    def get_count(
        self, session: Session, params: QueryParamsModel | None = None
    ) -> int:
        query = self.build_query(session, params)
        return query.count()
