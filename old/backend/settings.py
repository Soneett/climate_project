from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str = "orbits"
    db_user: str = "orbits_user"
    db_pass: str = "orbits_pass"
    db_port: int = 5432
    db_host: str = "127.0.0.1"

    def get_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.db_user}:{self.db_pass}@"
            f"{self.db_host}:{self.db_port}/"
            f"{self.db_name}"
        )


def get_settings() -> Settings:
    return Settings()
