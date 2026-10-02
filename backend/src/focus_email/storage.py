"""Lớp lưu trữ cục bộ cho các task được tạo từ email."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Optional

from focus_email.models import EmailMessage, EmailTask, TaskStatus, TaskUpdate


class TaskStorage:
    """Đọc, ghi và cập nhật ``tasks.json`` một cách tách biệt khỏi HTTP layer."""

    def __init__(self, storage_path: Optional[Path | str] = None) -> None:
        backend_dir = Path(__file__).resolve().parents[2]
        self.storage_path = Path(storage_path) if storage_path else backend_dir / "tasks.json"
        self._lock = RLock()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def load_all(self) -> list[EmailTask]:
        """Trả về toàn bộ task; kho chưa tạo được xem là rỗng."""
        with self._lock:
            if not self.storage_path.exists():
                return []
            try:
                with self.storage_path.open("r", encoding="utf-8") as file:
                    raw_tasks = json.load(file)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"tasks.json không phải JSON hợp lệ: {self.storage_path}") from exc

            if not isinstance(raw_tasks, list):
                raise RuntimeError("tasks.json phải chứa một mảng các task")
            return [EmailTask.model_validate(item) for item in raw_tasks]

    def save_all(self, tasks: list[EmailTask]) -> None:
        """Lưu toàn bộ task qua file tạm để tránh tạo JSON dở dang khi bị gián đoạn."""
        with self._lock:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
            payload = [task.model_dump(mode="json") for task in tasks]
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())
            temporary_path.replace(self.storage_path)

    def get_tasks(self, status: Optional[TaskStatus] = None) -> list[EmailTask]:
        tasks = self.load_all()
        return [task for task in tasks if task.status == status] if status else tasks

    def get_task_by_id(self, task_id: str) -> Optional[EmailTask]:
        return next((task for task in self.load_all() if task.task_id == task_id), None)

    def update_task(self, task_id: str, update_data: TaskUpdate) -> Optional[EmailTask]:
        """Cập nhật các trường được gửi lên và ghi lại thời gian cập nhật."""
        with self._lock:
            tasks = self.load_all()
            for index, task in enumerate(tasks):
                if task.task_id != task_id:
                    continue
                changes = update_data.model_dump(exclude_none=True)
                updated_task = task.model_copy(
                    update={**changes, "updated_at": self._now()}
                )
                tasks[index] = updated_task
                self.save_all(tasks)
                return updated_task
        return None

    def merge_emails(self, emails: list[dict]) -> tuple[int, int]:
        """Thêm email mới, nhưng giữ nguyên toàn bộ task đã có (smart merge)."""
        with self._lock:
            tasks = self.load_all()
            known_task_ids = {task.task_id for task in tasks}
            new_tasks = 0

            for email_data in emails:
                email = EmailMessage.model_validate(email_data)
                if email.id in known_task_ids:
                    continue
                now = self._now()
                tasks.append(
                    EmailTask(
                        task_id=email.id,
                        email=email,
                        created_at=now,
                        updated_at=now,
                    )
                )
                known_task_ids.add(email.id)
                new_tasks += 1

            if new_tasks:
                self.save_all(tasks)
            return len(emails), new_tasks
