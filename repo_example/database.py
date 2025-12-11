from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from settings import Settings, get_settings


class Database:
    def __init__(self, settings: Settings, echo: bool = False):
        self.settings = settings
        self.echo = echo
        self.engine = create_engine(settings.get_database_url(), echo=echo)
        self.maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_engine(self) -> Engine:
        return self.engine

    def session_generator(self):
        session = self.maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_session(self) -> Session:
        return next(self.session_generator())


db = Database(get_settings(), echo=False)
db_echo = Database(get_settings(), echo=True)
