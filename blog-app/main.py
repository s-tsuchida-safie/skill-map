from fastapi import FastAPI
from router import article, comment
from exception import exception_handlers

# FastAPIのインスタンス作成
app = FastAPI(exception_handlers=exception_handlers)
app.include_router(article.router)
app.include_router(comment.router)
