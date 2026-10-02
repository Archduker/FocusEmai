"""Export routers để entry point đăng ký API tập trung."""

from .auth import router as auth_router
from .sync import router as sync_router
from .tasks import router as tasks_router

__all__ = ["auth_router", "sync_router", "tasks_router"]
