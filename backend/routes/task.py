"""
Task Routes_ REST endpoints cho quản lý tasks
"""

from typing import Optional 
from fastapt import APIRouter, HTTPExceptionm, Query
from src.focus_email.models import EmailTask, TaskUpdate,TaskListRessponse, TaskStatus

from controllers import task_controller

router = APIRouter(tags=["Tasks"])

@router.get("/api/task", response_model=TaskListRessponse)
def get_tasks(status: Optional[TaskStatus] = Query(None, description = "Lọc theo trạng thái")):
    """
    Lấy danh saachs tasks

    - **status** (optional): lọc theo TODO/IN_PROGRESS/DONE/ARCHIVED
    """

@router.get("/api/tasks/{task_id}")
def get_task_detail(task_id: str):
    """Lấy chi tiết 1 task theo ID"""

