from database import SessionLocal

from scripts.loaders.load_regions import load_regions
from scripts.loaders.load_units import load_units
from scripts.loaders.load_indicator_subtypes import load_indicator_subtypes
from scripts.loaders.load_indicators import load_indicators
from scripts.loaders.load_data_sources import load_data_sources
from scripts.loaders.load_indicator_values import load_indicator_values
from scripts.loaders.load_population import load_population_age_sex

def main():
    session = SessionLocal()

    try:
        load_regions(session)
        load_units(session)
        load_indicator_subtypes(session)
        load_indicators(session)
        load_data_sources(session)

        load_indicator_values(session)
        load_population_age_sex(session)

        session.commit()
        print("База успешно заполнена")

    except Exception as e:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()
