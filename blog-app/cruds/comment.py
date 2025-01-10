from typing import List
from databases import Database
from model.comment import Comment
from utils.get_now_date_time import get_now_date_time


async def query_comments(db: Database, article_id: int, offset: int, limit: int):
    res = await db.fetch_one(
        query="""
      SELECT COUNT(*) AS `total` FROM `comment` WHERE article_id = :article_id ORDER BY created_at;""",
        values={"article_id": article_id},
    )
    total = res["total"]
    if offset > total:
        return {
            "total": total,
            "offset": offset,
            "count": 0,
            "list": [],
        }

    list = await db.fetch_all(
        query="""
          SELECT `comment_id`, `content` FROM `comment` ORDER BY created_at LIMIT :limit OFFSET :offset;""",
        values={"offset": offset, "limit": limit},
    )
    return {
        "total": total,
        "offset": offset,
        "count": len(list),
        "list": list,
    }


async def query_comment_by_id(db: Database, article_id: int, commnet_id: int):
    res = await db.fetch_one(
        query="""
      SELECT `article_id`, `comment_id`, `content`, `created_at` FROM `comment` WHERE `article_id` = :article_id AND `comment_id` = :comment_id;""",
        values={"article_id": article_id, "comment_id": commnet_id},
    )
    if res is None:
        return None

    return Comment(
        article_id=res["article_id"],
        comment_id=res["comment_id"],
        content=res["content"],
        created_at=res["created_at"],
    )


async def create_comment(db: Database, article_id: int, content: str):
    created_at = get_now_date_time()
    return await db.execute(
        """
      INSERT INTO `comment` (`article_id`, `content`, `created_at`) VALUES (:article_id, :content, :created_at);""",
        values={"article_id": article_id, "content": content, "created_at": created_at},
    )


async def delete_comments(db: Database, comment_ids: List[int]):
    await db.execute_many(
        query="""DELETE FROM `comment` WHERE `comment_id` = :comment_id;""",
        values=[{"comment_id": comment_id} for comment_id in comment_ids],
    )


async def update_comment(db: Database, comment_id: int, content: str):
    await db.execute(
        query="""
          UPDATE `comment` SET content = :content WHERE comment_id = :comment_id;""",
        values={"comment_id": comment_id, "content": content},
    )
