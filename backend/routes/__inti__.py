"""
Export tất cả routers để app.py dễ import
"""
from .tasks import router as tasks_router
from .sync import router as sync_router
from .auth import router as auth_router

__all__ = ["tasks_router", "sync_router", "auth_router"]