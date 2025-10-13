import pandas as pd

from database import db_echo
from tables import OrbitsTable
from models import CreateOrbitModel, OrbitModel
from repo import CreateRepo

DATA_PATH = "L1.Halo.csv"


def fill_data(path: str):
    repo = CreateRepo[OrbitsTable, OrbitModel, CreateOrbitModel](
        OrbitsTable, OrbitModel, CreateOrbitModel
    )

    data = pd.read_csv(path).to_dict(orient="records")
    items = [CreateOrbitModel.model_validate(element) for element in data]
    print(f"Filling {len(items)} orbits")

    session = db_echo.create_session()
    result = repo.bulk_create_records(items, session)
    print(f"Done...")


if __name__ == "__main__":
    fill_data(DATA_PATH)
