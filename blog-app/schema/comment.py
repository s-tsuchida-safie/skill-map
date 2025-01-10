from pydantic import BaseModel, Field
from typing import List


class ArticleCommentItem(BaseModel):
    comment_id: int = Field(title="コメントID")
    content: str = Field(title="コメントの中身")


class ArticleCommentListResponse(BaseModel):
    total: int = Field(title="検索結果の総数")
    offset: int = Field(title="返却リストのオフセット")
    count: int = Field(title="返却リストの件数")
    list: List[ArticleCommentItem] = Field(title="コメントの返却リスト")


class ArticleCommentPostRequest(BaseModel):
    content: str = Field(title="コメントの内容。1文字以上、400文字以下。")


class ArticleCommentPostResponse(BaseModel):
    comment_id: int = Field(title="コメントのID")
    content: str = Field(title="コメントの内容")


class ArticleCommentPatchRequest(BaseModel):
    content: str = Field(title="更新後のコメント内容。1文字以上、400文字以下。")


class ArticleCommentPatchResponse(BaseModel):
    status: str = Field(title="更新が成功したかどうかの結果")


class ArticleCommentDeleteRequest(BaseModel):
    comment_ids: List[int] = Field(title="削除する記事IDのリスト")


class ArticleCommentDeleteResponse(BaseModel):
    status: str = Field(title="削除が成功したかどうかの結果")
