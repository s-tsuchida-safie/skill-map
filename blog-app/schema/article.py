from pydantic import BaseModel, Field
from typing import List, Optional


class ArticleItem(BaseModel):
    article_id: int = Field(title="ブログ記事ID")
    title: str = Field(title="ブログ記事のタイトル")
    comment_count: int = Field(title="コメント数")


class ArticleListResponse(BaseModel):
    total: int = Field(title="検索結果の総数")
    offset: int = Field(title="返却リストのオフセット")
    count: int = Field(title="返却リストの件数")
    list: List[ArticleItem] = Field(title="記事の返却リスト")


class ArticleResponse(BaseModel):
    article_id: int = Field(title="ブログ記事ID")
    title: str = Field(title="ブログ記事のタイトル")
    content: str = Field(title="ブログ記事の中身")


class ArticlePostRequest(BaseModel):
    title: str = Field(title="ブログ記事のタイトル。1文字以上32文字以下")
    content: Optional[str] = Field(default="", title="ブログ記事の内容。2000文字以下。")


class ArticlePostResponse(BaseModel):
    article_id: int = Field(title="ブログ記事ID")
    title: str = Field(title="ブログ記事のタイトル")
    content: str = Field(title="ブログ記事の中身")


class ArticlePatchRequest(BaseModel):
    title: Optional[str] | None = Field(None, title="ブログ記事のタイトル。1文字以上32文字以下")
    content: Optional[str] | None = Field(None, title="ブログ記事の内容。2000文字以下。")


class ArticlePatchResponse(BaseModel):
    status: str = Field(title="結果")


class ArticleDeleteRequest(BaseModel):
    article_ids: List[int] = Field(title="削除する記事IDのリスト")


class ArticleDeleteResponse(BaseModel):
    status: str = Field(title="削除が成功したかどうかの結果")
