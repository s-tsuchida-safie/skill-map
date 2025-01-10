from databases import Database
from typing import List
from model.article import Article
from utils.get_now_date_time import get_now_date_time


async def query_articles(db: Database, offset: int, limit: int):
    res = await db.fetch_one(
        query="""
      SELECT COUNT(*) AS `total` FROM `article`"""
    )
    total = res["total"]
    if offset > total:
        return {
            "total": total,
            "offset": offset,
            "count": 0,
            "list": [],
        }

    listRes = await db.fetch_all(
        query="""
          SELECT `article_id`, `title` FROM `article` ORDER BY `created_at` LIMIT :limit OFFSET :offset;""",
        values={"offset": offset, "limit": limit},
    )
    list = []
    for row in listRes:
        article_id = row["article_id"]
        title = row["title"]
        res = await db.fetch_one(
            query="""SELECT COUNT(*) AS `count` FROM `comment` WHERE `article_id` = :article_id GROUP BY article_id;""",
            values={"article_id": article_id},
        )
        comment_count = 0
        if res is not None:
            comment_count = res["count"]

        list.append({"article_id": article_id, "title": title, "comment_count": comment_count})
    return {
        "total": total,
        "offset": offset,
        "count": len(list),
        "list": list,
    }


async def query_article_by_id(db: Database, article_id: int):
    res = await db.fetch_one(
        query="""
      SELECT `article_id`, `title`, `content`, `created_at` FROM `article` WHERE `article_id` = :article_id""",
        values={"article_id": article_id},
    )
    if res is None:
        return None

    return Article(
        article_id=res["article_id"], title=res["title"], content=res["content"], created_at=res["created_at"]
    )


async def create_article(db: Database, title: str, content: str):
    created_at = get_now_date_time()
    return await db.execute(
        """
    INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)""",
        values={"title": title, "content": content, "created_at": created_at},
    )


async def delete_articles(db: Database, article_ids: List[int]):
    await db.execute_many(
        query="""DELETE FROM `article` WHERE `article_id` = :article_id;""",
        values=[{"article_id": article_id} for article_id in article_ids],
    )


async def update_article(db: Database, article_id: int, title: str | None, content: str | None):
    set_params = []
    values = {"article_id": article_id}
    if title is not None:
        set_params.append("title = :title")
        values["title"] = title
    if content is not None:
        set_params.append("content = :content")
        values["content"] = content
    query = "UPDATE `article` SET " + ", ".join(set_params) + " WHERE article_id = :article_id"
    await db.execute(query=query, values=values)
