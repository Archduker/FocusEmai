"""
FocusEmail Package.
Cung cấp các công cụ kết nối Gmail, bóc tách email, mô hình hóa task và lưu trữ.
"""

from focus_email.auth import get_gmail_service
from focus_email.fetcher import fetch_recent_emails
from focus_email.models import (
    EmailMessage,
    EmailTask,
    TaskStatus,
    TaskPriority,
    TaskUpdate,
    AuthStatusResponse,
    TaskListResponse,
)

__all__ = [
    "get_gmail_service",
    "fetch_recent_emails",
    "EmailMessage",
    "EmailTask",
    "TaskStatus",
    "TaskPriority",
    "TaskUpdate",
    "AuthStatusResponse",
    "TaskListResponse",
]
