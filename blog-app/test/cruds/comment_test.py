import pytest
from utils.get_now_date_time import get_now_date_time


# @pytest.mark.asyncio
# async def test_query_comment(test_db):
#     created_at = get_now_date_time()
#     test_data = {"article_id": 1, "created_at": created_at, "content": "content3"}
#     await test_db.execute(
#         query="INSERT INTO `comment` (`article_id`, `content`, `created_at`) VALUES (:article_id, :content, :created_at)",
#         values=[
#             {"article_id": data["article_id"], "content": data["content"], "created_at": data["created_at"]}
#             for data in test_data
#         ],
#     )
