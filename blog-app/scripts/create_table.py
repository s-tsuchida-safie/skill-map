from databases import Database
import asyncio
import sys
import os

sys.path.append(os.getcwd())

from settings import get_settings

setting = get_settings()
db = Database(setting.database_url)


async def create_table(db: Database):
    await db.execute(query="DROP TABLE IF EXISTS article;")
    await db.execute(query="DROP TABLE IF EXISTS comment;")
    await db.execute(
        query="""
          CREATE TABLE article  (
              article_id INTEGER PRIMARY KEY AUTOINCREMENT,
              title VARCHAR(200) NOT NULL,
              content VARCHAR(10000) NOT NULL,
              created_at DATETIME NOT NULL);"""
    )
    await db.execute(
        query="""
          CREATE TABLE comment  (
              comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
              article_id INTEGER NOT NULL,
              content VARCHAR(2000) NOT NULL,
              created_at DATETIME NOT NULL,
              FOREIGN KEY (article_id) REFERENCES article(article_id));"""
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(create_table(db))
