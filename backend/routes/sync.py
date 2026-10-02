"""REST endpoint đồng bộ Gmail."""

from fastapi import APIRouter, HTTPException

from controllers import sync_controller

router = APIRouter(tags=["Sync"])


@router.post("/api/sync")
def sync_gmail() -> dict[str, int | str]:
    try:
        return sync_controller.sync_gmail_to_tasks()
    except (FileNotFoundError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
