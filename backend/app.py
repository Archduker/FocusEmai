"""
FastAPI Entry Point cho FocusEmail Backend.
Cung cấp RESTful API cho Frontend Next.js và tự động sinh Swagger Docs tại /docs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_router, sync_router, tasks_router

app = FastAPI(
    title="FocusEmail API",
    description="Backend RESTful API cho dự án FocusEmail (FastAPI + Next.js + Ollama)",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(sync_router)

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
