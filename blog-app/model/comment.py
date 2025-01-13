from pydantic import BaseModel, Field


class Comment(BaseModel):
    comment_id: int = Field(..., title="コメントID")
    article_id: int = Field(..., title="ブログ記事ID")
    content: str = Field(..., title="コメントの中身")
    created_at: str = Field(..., title="作成日時")
