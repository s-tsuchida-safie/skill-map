import typing
from settings import Settings, get_settings
from fastapi import Depends
from databases import Database


async def get_database(
    settings: Settings = Depends(get_settings),
) -> typing.AsyncGenerator[Database, None]:
    async with Database(settings.database_url) as db:
        await db.connect()
        yield db
