"""REST endpoints quản lý task."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from controllers import task_controller
from focus_email.models import EmailTask, TaskListResponse, TaskStatus, TaskUpdate

router = APIRouter(tags=["Tasks"])


@router.get("/api/tasks", response_model=TaskListResponse)
def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Lọc theo trạng thái"),
) -> TaskListResponse:
    tasks = task_controller.get_all_tasks(status_filter=status)
    return TaskListResponse(total=len(tasks), tasks=tasks)


@router.get("/api/tasks/{task_id}", response_model=EmailTask)
def get_task_detail(task_id: str) -> EmailTask:
    task = task_controller.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/api/tasks/{task_id}", response_model=EmailTask)
def update_task(task_id: str, update_data: TaskUpdate) -> EmailTask:
    updated_task = task_controller.update_task(task_id, update_data)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task
