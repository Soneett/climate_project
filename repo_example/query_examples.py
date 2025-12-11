from sqlalchemy.orm import Session

from database import db_echo
from tables import OrbitsTable
from models import QueryParamsModel, FilterModel, OrbitModel
from models import FilterOpEnum as Op
from repo import ReadRepo

QUERIES = {
    "All": QueryParamsModel(filters=[]),
    "Stable orbits": QueryParamsModel(
        filters=[FilterModel(field="stable", op=Op.eq, value=True)]
    ),
    "Cj": QueryParamsModel(
        filters=[
            FilterModel(field="cj", op=Op.ge, value=2.95),
            FilterModel(field="cj", op=Op.le, value=3.05),
        ]
    ),
    "First 100": QueryParamsModel(offset=0, limit=100),
    "Orbits with l1_im != 0": QueryParamsModel(
        filters=[FilterModel(field="l1_im", op=Op.ne, value=0)]
    ),
}


def run_examples(queries: dict[str, QueryParamsModel], session: Session):
    repo = ReadRepo[OrbitsTable, OrbitModel](OrbitsTable, OrbitModel)

    for name, query_params in queries.items():
        print("-----", name, "-----")
        print(f"Query filters: {query_params.filters}")
        print(f"Query offset, limit: {query_params.offset}, {query_params.limit}")
        orbits = repo.get_chunk(session, query_params)
        print(f"Count:", len(orbits))
        print(f"First record:")
        print(orbits[0])
        print(f"Last record:")
        print(orbits[-1])


if __name__ == "__main__":
    session = db_echo.create_session()
    run_examples(QUERIES, session)
