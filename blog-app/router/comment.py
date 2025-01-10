from fastapi import APIRouter, Depends, HTTPException
from database import get_database
from schema.comment import (
    ArticleCommentListResponse,
    ArticleCommentPostRequest,
    ArticleCommentPostResponse,
    ArticleCommentPatchRequest,
    ArticleCommentPatchResponse,
    ArticleCommentDeleteRequest,
    ArticleCommentDeleteResponse,
)
from databases import Database
from fastapi.param_functions import Body
from fastapi.params import Query, Path
from cruds.comment import (
    create_comment,
    query_comments,
    delete_comments,
    update_comment,
    query_comment_by_id,
)
from cruds.article import query_article_by_id
from exception import AppException, ErrorCode
from const import COMMENT_CONTENT_MAX_LENGTH

router = APIRouter()


@router.get(
    "/articles/{article_id}/comments",
    summary="指定されたブログ記事のコメントの一覧を取得する",
    response_model=ArticleCommentListResponse,
)
async def get_article_comments(
    article_id: int = Path(title="コメントされたブログ記事のID"),
    offset: int = Query(default=0, title="リストのオフセット"),
    limit: int = Query(
        default=50, title="リストの上限サイズ。0から100までの値をとり、デフォルトは50。"
    ),
    db: Database = Depends(get_database),
):
    article = await query_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(
            status_code=404, detail=f"article_id {article_id}が見つかりません"
        )
    if offset < 0:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.out_of_range,
            detail="offsetは0以上で指定してください",
        )
    if limit < 1 or limit > 100:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.out_of_range,
            detail="limitは0以上100以下で指定してください",
        )
    return await query_comments(db, article_id, offset, limit)


@router.post(
    "/articles/{article_id}/comments",
    summary="指定されたブログ記事のコメントを追加する",
    response_model=ArticleCommentPostResponse,
)
async def post_article_comments(
    article_id: int = Path(title="コメントされたブログ記事のID"),
    body: ArticleCommentPostRequest = Body(...),
    db: Database = Depends(get_database),
):
    article = await query_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(
            status_code=404, detail=f"article_id {article_id}が見つかりません"
        )

    content = body.content
    if len(content) == 0:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail="contentに空文字は指定できません",
        )
    if len(content) > COMMENT_CONTENT_MAX_LENGTH:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail=f"contentは{COMMENT_CONTENT_MAX_LENGTH}文字以内で指定してください",
        )

    comment_id = await create_comment(db, article_id, content)
    return ArticleCommentPostResponse(comment_id=comment_id, content=content)


@router.patch(
    "/articles/{article_id}/comments/{comment_id}",
    summary="コメントを更新する",
    response_model=ArticleCommentPatchResponse,
)
async def patch_article_comment(
    article_id: int = Path(title="コメントされたブログ記事のID"),
    comment_id: int = Path(title="コメントのID"),
    body: ArticleCommentPatchRequest = Body(...),
    db: Database = Depends(get_database),
):
    article = await query_article_by_id(db, article_id)
    print("article", article)
    if article is None:
        raise HTTPException(404, detail=f"article {article_id}が見つかりません")
    comment = await query_comment_by_id(db, article_id, comment_id)
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"article_id {article_id}内にcomment_id {comment_id}が見つかりません",
        )
    content = body.content
    if len(content) == 0:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail="contentに空文字は指定できません",
        )
    if len(content) > COMMENT_CONTENT_MAX_LENGTH:
        raise AppException(
            status_code=400,
            error_code=ErrorCode.invalid_format,
            detail=f"contentは{COMMENT_CONTENT_MAX_LENGTH}文字以内で指定してください",
        )

    await update_comment(db, content=content, comment_id=comment_id)
    return ArticleCommentPatchResponse(status="success")


@router.delete(
    "/articles/{article_id}/comments",
    summary="ブログ記事を削除する",
    response_model=ArticleCommentDeleteResponse,
)
async def delete_article_comment(
    article_id: int = Path(title="コメントされたブログ記事のID"),
    body: ArticleCommentDeleteRequest = Body(...),
    db: Database = Depends(get_database),
):
    article = await query_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(
            status_code=404, detail=f"article_id {article_id}が見つかりません"
        )

    comment_ids = body.comment_ids
    for comment_id in comment_ids:
        comment = await query_comment_by_id(db, article_id, comment_id)
        if comment is None:
            raise AppException(
                status_code=400,
                error_code=ErrorCode.invalid_format,
                detail=f"comment_id {comment_id}のアイテムは存在しません",
            )

    await delete_comments(db, body.comment_ids)
    return ArticleCommentDeleteResponse(status="success")
