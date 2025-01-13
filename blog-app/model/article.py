from pydantic import BaseModel, Field


class Article(BaseModel):
    article_id: int = Field(..., title="ブログ記事ID")
    title: str = Field(..., title="ブログ記事のタイトル")
    content: str = Field(..., title="ブログ記事の中身")
    created_at: str = Field(..., title="作成日時")
