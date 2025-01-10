from fastapi import APIRouter, Depends
from database import get_database
from schema.article import (
    ArticleListResponse,
    ArticlePostRequest,
    ArticlePostResponse,
    ArticleResponse,
    ArticlePatchRequest,
    ArticlePatchResponse,
    ArticleDeleteRequest,
    ArticleDeleteResponse,
)
from databases import Database
from fastapi.param_functions import Body
from fastapi.params import Query, Path
from cruds.article import query_articles, create_article, query_article_by_id, delete_articles, update_article
from exception import AppException, ErrorCode
from fastapi import HTTPException
from const import ARTICLE_TITLE_MAX_LENGTH, LIMIT_MAX, ARTICLE_CONTENT_MAX_LENGTH


router = APIRouter()


@router.get("/articles", summary="記事の一覧を取得する", response_model=ArticleListResponse)
async def get_articles(
    offset: int = Query(default=0, title="リストのオフセット"),
    limit: int = Query(default=50, title="リストの上限サイズ。0から100までの値をとり、デフォルトは50。"),
    db: Database = Depends(get_database),
) -> ArticleListResponse:
    if offset < 0:
        raise AppException(status_code=400, error_code=ErrorCode.out_of_range, detail="offsetは0以上で指定してください")
    if limit < 1 or limit > LIMIT_MAX:
        raise AppException(
            status_code=400, error_code=ErrorCode.out_of_range, detail=f"limitは0以上{LIMIT_MAX}以下で指定してください"
        )
    response = await query_articles(db, offset, limit)
    return response


@router.get(
    "/articles/{article_id}",
    summary="記事の詳細情報を取得する",
    response_model=ArticleResponse,
)
async def get_article_by_id(
    article_id: int = Path(title="ブログ記事ID"),
    db: Database = Depends(get_database),
):
    article = await query_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail=f"article_id {article_id}が見つかりません")
    return ArticleResponse(article_id=article.article_id, title=article.title, content=article.content)


@router.post("/articles", summary="ブログ記事を作成する", response_model=ArticlePostResponse)
async def post_articles(
    body: ArticlePostRequest = Body(...),
    db: Database = Depends(get_database),
):
    title = body.title
    if len(title) == 0:
        raise AppException(status_code=400, error_code=ErrorCode.invalid_format, detail="titleに空文字は指定できません")
    if len(title) > ARTICLE_TITLE_MAX_LENGTH:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail=f"titleは{ARTICLE_TITLE_MAX_LENGTH}文字以内で指定してください",
        )

    content = body.content
    if content is not None and len(content) > ARTICLE_CONTENT_MAX_LENGTH:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail=f"contentは{ARTICLE_CONTENT_MAX_LENGTH}文字以内で指定してください",
        )

    article_id = await create_article(db, title, content)
    return ArticlePostResponse(article_id=article_id, title=title, content=content)


@router.patch(
    "/articles/{article_id}",
    summary="ブログ記事を更新する",
    response_model=ArticlePatchResponse,
)
async def patch_article(
    article_id: int = Path(title="ブログ記事ID"),
    body: ArticlePatchRequest = Body(...),
    db: Database = Depends(get_database),
):
    article = await query_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail=f"article_id {article_id}が見つかりません")

    title = body.title
    if title is not None and len(title) == 0:
        raise AppException(status_code=400, error_code=ErrorCode.invalid_format, detail="titleに空文字は指定できません")
    if title is not None and len(title) > ARTICLE_TITLE_MAX_LENGTH:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail=f"titleは{ARTICLE_TITLE_MAX_LENGTH}文字以内で指定してください",
        )

    content = body.content
    if content is not None and len(content) > ARTICLE_CONTENT_MAX_LENGTH:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail=f"contentは{ARTICLE_CONTENT_MAX_LENGTH}文字以内で指定してください",
        )

    await update_article(db, article_id=article_id, title=title, content=content)
    return ArticlePatchResponse(status="success")


@router.delete("/articles", summary="ブログ記事を削除する", response_model=ArticleDeleteResponse)
async def delete_article(
    body: ArticleDeleteRequest = Body(...),
    db: Database = Depends(get_database),
):
    article_ids = body.article_ids
    for article_id in article_ids:
        article = await query_article_by_id(db, article_id)
        if article is None:
            raise AppException(
                status_code=400,
                error_code=ErrorCode.invalid_format,
                detail=f"article_id {article_id}のアイテムは存在しません",
            )
    await delete_articles(db, body.article_ids)
    return ArticleDeleteResponse(status="success")
