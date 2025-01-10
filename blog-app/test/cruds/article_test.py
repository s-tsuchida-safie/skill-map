import pytest
from cruds.article import query_articles
from utils.get_now_date_time import get_now_date_time


@pytest.mark.asyncio
async def test_query_articles(test_db):
    created_at = get_now_date_time()
    test_data = [
        {"title": "title1", "created_at": created_at, "content": "content1"},
        {"title": "title2", "created_at": created_at, "content": "content2"},
        {"title": "title3", "created_at": created_at, "content": "content3"},
    ]
    await test_db.execute_many(
        query="INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)",
        values=[
            {"title": data["title"], "content": data["content"], "created_at": data["created_at"]} for data in test_data
        ],
    )
    # offset > totalの場合
    res = await query_articles(test_db, 4, 1)
    assert res["total"] == 3
    assert res["offset"] == 4
    assert res["count"] == 0
    assert len(res["list"]) == 0
