import pytest
from utils.get_now_date_time import get_now_date_time


@pytest.mark.asyncio
async def test_get_articles(test_db, test_client):
    created_at = get_now_date_time()
    test_data = [
        {"title": "title1", "created_at": created_at, "content": "content1"},
        {"title": "title2", "created_at": created_at, "content": "content2"},
        {"title": "title3", "created_at": created_at, "content": "content3"},
    ]
    await test_db.execute_many(
        query="INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)",
        values=[
            {
                "title": data["title"],
                "content": data["content"],
                "created_at": data["created_at"],
            }
            for data in test_data
        ],
    )
    # クエリパラメータなしでリクエストする
    res = test_client.get("/articles")
    assert res.status_code == 200
    resBody = res.json()
    assert resBody["total"] == 3
    assert resBody["count"] == 3
    assert resBody["offset"] == 0
    assert len(resBody["list"]) == 3

    # offset, limitを指定して、リクエストする
    res = test_client.get("/articles", params={"offset": 1, "limit": 1})
    assert res.status_code == 200
    resBody = res.json()
    assert resBody["total"] == 3
    assert resBody["count"] == 1
    assert resBody["offset"] == 1
    assert len(resBody["list"]) == 1

    # offsetを0以下の値を指定してリクエストする
    res = test_client.get("/articles", params={"offset": -1})
    assert res.status_code == 400
    assert res.json()["error_code"] == "out_of_range"

    # limitを1から100までの範囲外の値を指定してリクエストする
    res = test_client.get("/articles", params={"limit": 1000})
    assert res.status_code == 400
    assert res.json()["error_code"] == "out_of_range"

    res = test_client.get("/articles", params={"limit": 0})
    assert res.status_code == 400
    assert res.json()["error_code"] == "out_of_range"


@pytest.mark.asyncio
async def test_get_article(test_db, test_client):
    created_at = get_now_date_time()
    test_data = {
        "title": "title_test",
        "created_at": created_at,
        "content": "content_test",
    }
    id = await test_db.execute(
        query="INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)",
        values={
            "title": test_data["title"],
            "content": test_data["content"],
            "created_at": test_data["created_at"],
        },
    )

    # DB上に存在するarticle_idでリクエストする
    res = test_client.get("/articles/" + str(id))
    assert res.status_code == 200
    resBody = res.json()
    assert resBody["article_id"] == id
    assert resBody["title"] == test_data["title"]
    assert resBody["content"] == test_data["content"]

    # 存在しないarticle_idでリクエストする
    res = test_client.get("/articles/" + str(-1))
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_post_article(test_db, test_client):
    # titleを正常な値で指定してリクエストする
    req_body = {"title": "title1"}
    res = test_client.post("/articles", json=req_body)
    assert res.status_code == 200
    db_res = await test_db.fetch_one(
        query="SELECT `title`, `content` FROM `article` WHERE `title` = :title",
        values={"title": req_body["title"]},
    )
    assert db_res != None
    assert db_res["title"] == req_body["title"]
    assert db_res["content"] == ""
    await test_db.execute(
        query="DELETE FROM `article` WHERE `title` = :title",
        values={"title": req_body["title"]},
    )

    # titleを指定せずにリクエストする
    req_body = {"content": "content1"}
    res = test_client.post("/articles", json=req_body)
    assert res.status_code == 422

    # titleを空文字でリクエストする
    req_body = {"title": "", "content": "content1"}
    res = test_client.post("/articles", json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"

    # titleを33文字以上でリクエストする
    req_body = {"title": "1" * 33, "content": "content1"}
    res = test_client.post("/articles", json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"

    # contentを正常な値で指定してリクエストする
    req_body = {"title": "title1", "content": "content1"}
    res = test_client.post("/articles", json=req_body)
    assert res.status_code == 200
    db_res = await test_db.fetch_all(query="SELECT `title`, `content` FROM `article`")
    assert len(db_res) == 1
    assert db_res[0]["title"] == req_body["title"]
    assert db_res[0]["content"] == req_body["content"]
    await test_db.execute(
        query="DELETE FROM `article` WHERE `title` = :title",
        values={"title": req_body["title"]},
    )

    # contentを2001文字以上でリクエストする
    req_body = {"title": "title1", "content": "c" * 2001}
    res = test_client.post("/articles", json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"


@pytest.mark.asyncio
async def test_patch_article(test_db, test_client):
    created_at = get_now_date_time()
    default_title = "default_title"
    default_content = "default_content"
    article_id = await test_db.execute(
        query="INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)",
        values={
            "title": default_title,
            "content": default_content,
            "created_at": created_at,
        },
    )

    # 存在しないarticle_idでリクエストする
    req_body = {}
    res = test_client.patch("/articles/" + str(article_id + 1), json=req_body)
    assert res.status_code == 404

    # titleのみ指定してリクエストする
    req_body = {"title": "new_title"}
    res = test_client.patch("/articles/" + str(article_id), json=req_body)
    db_res = await test_db.fetch_one(
        query="SELECT * FROM `article` WHERE `article_id` = :article_id",
        values={"article_id": article_id},
    )
    assert db_res["title"] == req_body["title"]
    assert db_res["content"] == default_content
    await test_db.execute(
        query="UPDATE `article` SET `title` = :title, `content` = :content WHERE `article_id` = :article_id;",
        values={
            "title": default_title,
            "content": default_content,
            "article_id": article_id,
        },
    )

    # titleを空文字でリクエストする
    req_body = {"title": ""}
    res = test_client.patch("/articles/" + str(article_id), json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"

    # titleを33文字以上でリクエストする
    req_body = {"title": "1" * 33}
    res = test_client.patch("/articles/" + str(article_id), json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"

    # contentのみ指定してリクエストする
    req_body = {"content": "new_content"}
    res = test_client.patch("/articles/" + str(article_id), json=req_body)
    db_res = await test_db.fetch_one(
        query="SELECT * FROM `article` WHERE `article_id` = :article_id",
        values={"article_id": article_id},
    )
    assert db_res["title"] == default_title
    assert db_res["content"] == req_body["content"]
    await test_db.execute(
        query="UPDATE `article` SET `title` = :title, `content` = :content WHERE `article_id` = :article_id;",
        values={
            "title": default_title,
            "content": default_content,
            "article_id": article_id,
        },
    )

    # contentを2001文字以上でリクエストする
    req_body = {"content": "1" * 2001}
    res = test_client.patch("/articles/" + str(article_id), json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"

    # titleとcontentの両方を指定してリクエストする
    req_body = {"title": "new_title", "content": "new_content"}
    res = test_client.patch("/articles/" + str(article_id), json=req_body)
    db_res = await test_db.fetch_one(
        query="SELECT * FROM `article` WHERE `article_id` = :article_id",
        values={"article_id": article_id},
    )
    assert db_res["title"] == req_body["title"]
    assert db_res["content"] == req_body["content"]
    await test_db.execute(
        query="UPDATE `article` SET `title` = :title, `content` = :content WHERE `article_id` = :article_id;",
        values={
            "title": default_title,
            "content": default_content,
            "article_id": article_id,
        },
    )


@pytest.mark.asyncio
async def test_delete_articles(test_db, test_client):
    # DB上に存在するarticle_idでリクエストする
    created_at = get_now_date_time()
    test_data = {
        "title": "title_test",
        "created_at": created_at,
        "content": "content_test",
    }
    article_id = await test_db.execute(
        query="INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)",
        values={
            "title": test_data["title"],
            "content": test_data["content"],
            "created_at": test_data["created_at"],
        },
    )
    req_body = {"article_ids": [article_id]}
    res = test_client.request("DELETE", "/articles", json=req_body)
    assert res.status_code == 200

    # 存在しないarticle_idでリクエストする
    created_at = get_now_date_time()
    test_data = {
        "title": "title_test",
        "created_at": created_at,
        "content": "content_test",
    }
    article_id = await test_db.execute(
        query="INSERT INTO `article` (`title`, `content`, `created_at`) VALUES (:title, :content, :created_at)",
        values={
            "title": test_data["title"],
            "content": test_data["content"],
            "created_at": test_data["created_at"],
        },
    )
    req_body = {"article_ids": [article_id + 100]}
    res = test_client.request("DELETE", "/articles", json=req_body)
    assert res.status_code == 400
    assert res.json()["error_code"] == "invalid_format"
