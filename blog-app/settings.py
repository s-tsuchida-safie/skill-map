import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    database_url: str = "sqlite+aiosqlite:///app.db"
    test_database_url: str = "sqlite+aiosqlite:///./test/test_app.db"


def get_settings():
    return Settings()
