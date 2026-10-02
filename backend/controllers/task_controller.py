"""Business logic cho việc đọc và cập nhật task."""

from typing import Optional

from focus_email.models import EmailTask, TaskStatus, TaskUpdate
from focus_email.storage import TaskStorage

storage = TaskStorage()


def get_all_tasks(status_filter: Optional[TaskStatus] = None) -> list[EmailTask]:
    return storage.get_tasks(status_filter)


def get_task_by_id(task_id: str) -> Optional[EmailTask]:
    return storage.get_task_by_id(task_id)


def update_task(task_id: str, update_data: TaskUpdate) -> Optional[EmailTask]:
    return storage.update_task(task_id, update_data)
