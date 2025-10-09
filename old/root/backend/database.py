from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def init_db():
    with engine.begin() as conn: 
        #схемы
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS ref AUTHORIZATION climate_user;")) #справочники
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS core AUTHORIZATION climate_user;")) #рабочие данные
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging AUTHORIZATION climate_user;")) #загрузка данных

        #роли
        conn.execute(text("CREATE ROLE IF NOT EXISTS app_reader NOINHERIT;"))
        conn.execute(text("CREATE ROLE IF NOT EXISTS app_editor NOINHERIT;"))
        conn.execute(text("CREATE ROLE IF NOT EXISTS app_admin NOINHERIT;"))

        #права на схемы
        conn.execute(text("GRANT USAGE ON SCHEMA ref, core TO app_reader, app_editor, app_admin;"))

        conn.execute(text("""
            ALTER DEFAULT PRIVILEGES IN SCHEMA ref
            GRANT SELECT ON TABLES TO app_reader;
            ALTER DEFAULT PRIVILEGES IN SCHEMA core
            GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_editor;
            ALTER DEFAULT PRIVILEGES IN SCHEMA core
            GRANT USAGE, SELECT ON SEQUENCES TO app_editor;
            ALTER DEFAULT PRIVILEGES IN SCHEMA ref
            GRANT USAGE, SELECT ON SEQUENCES TO app_editor;
        """))

        conn.execute(text("CREATE ROLE IF NOT EXISTS u_admin LOGIN PASSWORD 'admin_pass';"))
        conn.execute(text("CREATE ROLE IF NOT EXISTS u_editor LOGIN PASSWORD 'editor_pass';"))
        conn.execute(text("CREATE ROLE IF NOT EXISTS u_reader LOGIN PASSWORD 'reader_pass';"))

        conn.execute(text("GRANT app_admin TO u_admin;"))
        conn.execute(text("GRANT app_editor TO u_editor;"))
        conn.execute(text("GRANT app_reader TO u_reader;"))

        conn.execute(text("ALTER ROLE u_editor SET search_path = core, ref, public;"))
        conn.execute(text("ALTER ROLE u_reader SET search_path = core, ref, public;"))




