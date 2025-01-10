from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from enum import Enum
from typing import Any, Dict, Optional


class ErrorCode(str, Enum):
    out_of_range = "out_of_range"  # 範囲外を指定
    invalid_format = "invalid_format"  # 不正なフォーマット
    no_required_param = "no_required_param"  # 必要なパラメータがない


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
        error_code: ErrorCode = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


async def exception_handler(request: Request, exc: AppException) -> JSONResponse:
    body = {"detail": exc.detail, "error_code": exc.error_code}
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        body, status_code=exc.status_code, headers=headers if headers else None
    )


exception_handlers = {AppException: exception_handler}
