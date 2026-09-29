"""
Main entry point cho FocusEmail - Stage 1 CLI Runner.
Kết nối Gmail API, quét các email trong 7 ngày gần nhất và hiển thị dạng thẻ trên Terminal.
"""

from focus_email.auth import get_gmail_service
from focus_email.fetcher import fetch_recent_emails


def print_divider(char: str = "=", length: int = 80):
    print(char * length)


def display_email_card(index: int, email: dict):
    print_divider("=")
    print(f"📩 [{index}] TIÊU ĐỀ: {email.get('subject', '(Không có tiêu đề)')}")
    print(f"👤 TỪ: {email.get('sender_name')} <{email.get('sender_email')}>")
    print(f"📥 ĐẾN: {email.get('recipient', 'N/A')}")
    print(f"📅 NGÀY: {email.get('date', 'N/A')}")
    labels = ", ".join(email.get("labels", []))
    status_icon = "🔴 CHƯA ĐỌC" if email.get("is_unread") else "🟢 ĐÃ ĐỌC"
    print(f"🏷️ NHÃN: {labels} ({status_icon})")
    print_divider("-")
    print(f"💬 TRÍCH DẪN: {email.get('snippet', '')}")

    # Bóc tách và hiển thị 5 dòng đầu của nội dung
    body_text = email.get("body_text", "")
    lines = [line.strip() for line in body_text.splitlines() if line.strip()]
    if lines:
        preview = "\n   ".join(lines[:5])
        print(f"📝 NỘI DUNG CHÍNH (5 dòng đầu):\n   {preview}")
    else:
        print("📝 NỘI DUNG CHÍNH: (Thư không có nội dung chữ thuần)")
    print_divider("=")
    print()


def main():
    print_divider("=")
    print("🚀 FOCUS EMAIL - STAGE 1 CLI RUNNER")
    print("Hệ thống lọc & quản lý email tập trung")
    print_divider("=")
    print("⏳ Đang kết nối Gmail API và quét các email trong 7 ngày gần nhất...")

    try:
        service = get_gmail_service()
        emails = fetch_recent_emails(service, max_results=5)

        if not emails:
            print("\n⚠️ 0 email được tìm thấy trong 7 ngày gần nhất.")
            return

        print(f"\n🎉 Thành công! Tìm thấy {len(emails)} email gần nhất:\n")
        for i, email in enumerate(emails, start=1):
            display_email_card(i, email)

    except Exception as e:
        print(f"\n❌ Đã xảy ra lỗi: {e}")


if __name__ == "__main__":
    main()
