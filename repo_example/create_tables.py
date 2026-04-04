from sqlalchemy import MetaData, text

from tables import Base
from database import db_echo


def main():
    engine = db_echo.get_engine()

    metadata = MetaData()
    metadata.reflect(engine)

    print("Database table list:")
    db_tables = list(metadata.tables.keys())
    print(db_tables)

    print("Current table list:")
    cur_tables = list(Base.metadata.tables.keys())
    print(cur_tables)

    print("Removed tables in current version:")
    print(set(db_tables) - set(cur_tables))

    print("New tables in current version:")
    print(set(cur_tables) - set(db_tables))

    print("Dropping...")
    with engine.begin() as conn:
        for table in reversed(metadata.sorted_tables):
            conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))
            print(f"{table.name} dropped")

    print("Creating...")
    Base.metadata.create_all(engine)

    print("All done!")


if __name__ == "__main__":
    main()
