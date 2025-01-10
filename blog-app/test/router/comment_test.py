import pytest
from utils.get_now_date_time import get_now_date_time


async def create_article(db):
    created_at = get_now_date_time()
    test_data = {
        "title": "title_test",
        "created_at": created_at,
        "content": "content_test",
    }
    article_id = await db.execute(
        query="INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)",
        values={
            "title": test_data["title"],
            "content": test_data["content"],
            "created_at": test_data["created_at"],
        },
    )
    return article_id


@pytest.mark.asyncio
async def test_get_comments(test_db, test_client):
    created_at = get_now_date_time()
    article_id = await create_article(test_db)
    test_data = [
        {"article_id": article_id, "created_at": created_at, "content": "content1"},
        {"article_id": article_id, "created_at": created_at, "content": "content2"},
        {"article_id": article_id, "created_at": created_at, "content": "content3"},
    ]
    await test_db.execute_many(
        query="INSERT INTO `comment` (`article_id`, `content`, `created_at`) VALUES (:article_id, :content, :created_at)",
        values=[
            {
                "article_id": data["article_id"],
                "content": data["content"],
                "created_at": data["created_at"],
            }
            for data in test_data
        ],
    )
    # DB上に存在しないarticle_idでリクエストする
    res = test_client.get("/articles/" + str(article_id + 1) + "/comments")
    assert res.status_code == 404

    # クエリパラメータなしでリクエストする
    res = test_client.get("/articles/" + str(article_id) + "/comments")
    assert res.status_code == 200
    resBody = res.json()
    assert resBody["total"] == 3
    assert resBody["count"] == 3
    assert resBody["offset"] == 0
    assert len(resBody["list"]) == 3

    # offset, limitを指定して、リクエストする
    res = test_client.get(
        "/articles/" + str(article_id) + "/comments", params={"offset": 1, "limit": 1}
    )
    assert res.status_code == 200
    resBody = res.json()
    assert resBody["total"] == 3
    assert resBody["count"] == 1
    assert resBody["offset"] == 1
    assert len(resBody["list"]) == 1

    # offsetを0以下の値を指定してリクエストする
    res = test_client.get(
        "/articles/" + str(article_id) + "/comments", params={"offset": -1}
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "out_of_range"

    # limitを1から100までの範囲外の値を指定してリクエストする
    res = test_client.get(
        "/articles/" + str(article_id) + "/comments", params={"limit": 1000}
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "out_of_range"

    res = test_client.get(
        "/articles/" + str(article_id) + "/comments", params={"limit": 0}
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "out_of_range"


@pytest.mark.asyncio
async def test_post_comments(test_db, test_client):
    article_id = await create_article(test_db)

    # DB上に存在しないarticle_idでリクエストする
    req_body = {"content": "content1"}
    res = test_client.post(
        "/articles/" + str(article_id + 100) + "/comments", json=req_body
    )
    assert res.status_code == 404

    # contentを指定してリクエストする
    req_body = {"content": "content1"}
    res = test_client.post("/articles/" + str(article_id) + "/comments", json=req_body)
    assert res.status_code == 200
    db_res = await test_db.fetch_one(
        query="SELECT `content` FROM `comment` WHERE `content` = :content;",
        values={"content": req_body["content"]},
    )
    assert db_res != None
    assert db_res["content"] == req_body["content"]
    await test_db.execute(
        query="DELETE FROM `article` WHERE `title` = :title", values={"title": "title1"}
    )

    # contentを指定せずにリクエストする
    req_body = {}
    res = test_client.post("/articles/" + str(article_id) + "/comments", json=req_body)
    assert res.status_code == 422

    # contentを空文字でリクエストする
    req_body = {"content": ""}
    res = test_client.post("/articles/" + str(article_id) + "/comments", json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"

    # contentを401文字以上でリクエストする
    req_body = {"content": "1" * 401}
    res = test_client.post("/articles/" + str(article_id) + "/comments", json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"


@pytest.mark.asyncio
async def test_patch_comments(test_db, test_client):
    article_id = await create_article(test_db)
    created_at = get_now_date_time()
    default_content = "default_content"
    comment_id = await test_db.execute(
        query="INSERT INTO `comment` (`article_id`, `content`, `created_at`) VALUES (:article_id, :content, :created_at)",
        values={
            "article_id": article_id,
            "content": default_content,
            "created_at": created_at,
        },
    )

    new_content = "new_content"

    # DB上に存在しないarticle_idでリクエストする
    req_body = {"content": new_content}
    res = test_client.patch(
        "/articles/" + str(article_id + 100) + "/comments/" + str(comment_id),
        json=req_body,
    )
    assert res.status_code == 404

    # DB上に存在しないcomment_idでリクエストする
    req_body = {"content": new_content}
    res = test_client.patch(
        "/articles/" + str(article_id) + "/comments/" + str(comment_id + 100),
        json=req_body,
    )
    assert res.status_code == 404

    # contentを指定してリクエストする
    req_body = {"content": new_content}
    res = test_client.patch(
        "/articles/" + str(article_id) + "/comments/" + str(comment_id), json=req_body
    )
    assert res.status_code == 200
    db_res = await test_db.fetch_one(
        query="SELECT `content` FROM `comment` WHERE `comment_id` = :comment_id;",
        values={"comment_id": comment_id},
    )
    assert db_res != None
    assert db_res["content"] == req_body["content"]

    # contentを指定せずにリクエストする
    req_body = {}
    res = test_client.patch(
        "/articles/" + str(article_id) + "/comments/" + str(comment_id), json=req_body
    )
    assert res.status_code == 422

    # contentに空文字を指定してリクエストする
    req_body = {"content": ""}
    res = test_client.patch(
        "/articles/" + str(article_id) + "/comments/" + str(comment_id), json=req_body
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"

    # contentを401文字以上でリクエストする
    req_body = {"content": "1" * 401}
    res = test_client.patch(
        "/articles/" + str(article_id) + "/comments/" + str(comment_id), json=req_body
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"


@pytest.mark.asyncio
async def test_delete_comments(test_db, test_client):
    article_id = await create_article(test_db)
    created_at = get_now_date_time()
    default_content = "default_content"
    comment_id = await test_db.execute(
        query="INSERT INTO `comment` (`article_id`, `content`, `created_at`) VALUES (:article_id, :content, :created_at)",
        values={
            "article_id": article_id,
            "content": default_content,
            "created_at": created_at,
        },
    )

    # DB上に存在しないarticle_idでリクエストする
    req_body = {"comment_ids": [comment_id]}
    res = test_client.request(
        "DELETE", "/articles/" + str(article_id + 100) + "/comments", json=req_body
    )
    assert res.status_code == 404

    # comment_idsを指定してリクエストする
    req_body = {"comment_ids": [comment_id]}
    res = test_client.request(
        "DELETE", "/articles/" + str(article_id) + "/comments", json=req_body
    )
    assert res.status_code == 200

    # comment_idsにDBに存在しないcomment_idを指定してリクエストする
    article_id = await create_article(test_db)
    created_at = get_now_date_time()
    default_content = "default_content"
    comment_id = await test_db.execute(
        query="INSERT INTO `comment` (`article_id`, `content`, `created_at`) VALUES (:article_id, :content, :created_at)",
        values={
            "article_id": article_id,
            "content": default_content,
            "created_at": created_at,
        },
    )
    req_body = {"comment_ids": [comment_id + 100]}
    res = test_client.request(
        "DELETE", "/articles/" + str(article_id) + "/comments", json=req_body
    )
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"
