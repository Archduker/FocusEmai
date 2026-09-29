"""
FastAPI Entry Point cho FocusEmail Backend.
Cung cấp RESTful API cho Frontend Next.js và tự động sinh Swagger Docs tại /docs.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from focus_email.models import (
    AuthStatusResponse,
    TaskListResponse,
    EmailTask,
    EmailMessage,
    TaskStatus,
    TaskPriority,
)

app = FastAPI(
    title="FocusEmail API",
    description="Backend RESTful API cho dự án FocusEmail (FastAPI + Next.js + Ollama)",
    version="0.1.0",
)

# Cấu hình CORS để Frontend Next.js (chạy ở port 3000) có thể gọi API mà không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def read_root():
    """Kiểm tra server có đang hoạt động hay không."""
    return {
        "status": "online",
        "service": "FocusEmail Backend",
        "docs_url": "/docs",
    }


@app.get("/api/status", response_model=AuthStatusResponse, tags=["Auth"])
def get_auth_status():
    """Kiểm tra trạng thái đăng nhập Gmail OAuth2."""
    from focus_email.auth import _resolve_path
    token_file = _resolve_path("token.json")
    has_token = os.path.exists(token_file)
    return AuthStatusResponse(
        authenticated=has_token,
        user_email="t20067771@gmail.com" if has_token else None,
    )
