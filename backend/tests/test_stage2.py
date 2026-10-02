"""Các test hồi quy tối thiểu cho chức năng Stage 2."""

import tempfile
import unittest
from pathlib import Path

from fastapi import HTTPException

from app import app
from controllers import task_controller
from focus_email.models import TaskStatus, TaskUpdate
from focus_email.storage import TaskStorage
from routes.tasks import get_task_detail, get_tasks, update_task


def sample_email(email_id: str = "mail-1") -> dict:
    return {
        "id": email_id,
        "thread_id": "thread-1",
        "sender_name": "Nguyễn Văn A",
        "sender_email": "a@example.com",
        "recipient": "me@example.com",
        "subject": "Việc cần xử lý",
        "date": "Fri, 02 Oct 2026 10:00:00 +0000",
    }


class TaskStorageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = TaskStorage(Path(self.temp_dir.name) / "tasks.json")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_merge_preserves_existing_task_fields(self) -> None:
        self.assertEqual(self.storage.merge_emails([sample_email()]), (1, 1))
        updated = self.storage.update_task(
            "mail-1", TaskUpdate(status=TaskStatus.DONE, notes="Đã trả lời")
        )
        self.assertIsNotNone(updated)

        self.assertEqual(self.storage.merge_emails([sample_email("mail-1")]), (1, 0))
        task = self.storage.get_task_by_id("mail-1")
        assert task is not None
        self.assertEqual(task.status, TaskStatus.DONE)
        self.assertEqual(task.notes, "Đã trả lời")

    def test_filter_and_missing_task(self) -> None:
        self.storage.merge_emails([sample_email("mail-1"), sample_email("mail-2")])
        self.storage.update_task("mail-2", TaskUpdate(status=TaskStatus.IN_PROGRESS))
        self.assertEqual(len(self.storage.get_tasks(TaskStatus.TODO)), 1)
        self.assertIsNone(self.storage.update_task("does-not-exist", TaskUpdate(notes="x")))


class TaskRoutesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_storage = task_controller.storage
        task_controller.storage = TaskStorage(Path(self.temp_dir.name) / "tasks.json")
        task_controller.storage.merge_emails([sample_email()])

    def tearDown(self) -> None:
        task_controller.storage = self.original_storage
        self.temp_dir.cleanup()

    def test_list_patch_detail_and_404(self) -> None:
        response = get_tasks(TaskStatus.TODO)
        self.assertEqual(response.total, 1)

        response = update_task("mail-1", TaskUpdate(status=TaskStatus.DONE))
        self.assertEqual(response.status, TaskStatus.DONE)

        self.assertEqual(get_task_detail("mail-1").task_id, "mail-1")
        with self.assertRaises(HTTPException) as caught:
            update_task("missing", TaskUpdate())
        self.assertEqual(caught.exception.status_code, 404)

    def test_openapi_contains_all_stage_2_paths(self) -> None:
        self.assertTrue(
            {"/", "/api/status", "/api/tasks", "/api/tasks/{task_id}", "/api/sync"}
            <= set(app.openapi()["paths"])
        )


if __name__ == "__main__":
    unittest.main()
