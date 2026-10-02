"""Business logic đồng bộ Gmail vào kho task cục bộ."""

from focus_email.auth import get_gmail_service
from focus_email.fetcher import fetch_recent_emails
from focus_email.storage import TaskStorage

storage = TaskStorage()


def sync_gmail_to_tasks() -> dict[str, int | str]:
    service = get_gmail_service()
    emails = fetch_recent_emails(service, max_results=10, days_back=7)
    total_synced, new_added = storage.merge_emails(emails)
    return {
        "message": "Đồng bộ thành công!",
        "total_synced": total_synced,
        "new_tasks_added": new_added,
    }
