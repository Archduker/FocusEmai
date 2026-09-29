import base64
from email.utils import parseaddr
from bs4 import BeautifulSoup


def decode_body(payload: dict) -> tuple[str, str]:
    """
    Giải mã payload của Gmail API để lấy nội dung text thuần (body_text) và HTML (body_html).

    Args:
        payload (dict): Payload của message từ Gmail API (chứa body hoặc parts).

    Returns:
        tuple[str, str]: (body_text, body_html)
    """
    body_text = ""
    body_html = ""

    def extract_parts(part: dict):
        nonlocal body_text, body_html
        mime_type = part.get("mimeType", "")
        body = part.get("body", {})
        data = body.get("data")

        if data:
            try:
                # Xử lý bù padding cho Base64 URL-safe nếu thiếu ký tự '='
                padded_data = data + "=" * (-len(data) % 4)
                decoded_bytes = base64.urlsafe_b64decode(padded_data)
                text_content = decoded_bytes.decode("utf-8", errors="ignore")

                if mime_type == "text/plain":
                    body_text += text_content + "\n"
                elif mime_type == "text/html":
                    body_html += text_content + "\n"
            except Exception:
                pass

        # Đệ quy duyệt qua các phần con nếu có multipart
        for sub_part in part.get("parts", []):
            extract_parts(sub_part)

    extract_parts(payload)

    # Nếu không có text thuần nhưng có HTML, dùng BeautifulSoup để bóc tách text
    if not body_text.strip() and body_html.strip():
        soup = BeautifulSoup(body_html, "html.parser")
        body_text = soup.get_text(separator="\n")

    return (body_text.strip(), body_html.strip())


def parse_email_message(msg_detail: dict) -> dict:
    """
    Trích xuất và chuẩn hóa thông tin chi tiết của một email từ Gmail API.

    Args:
        msg_detail (dict): Dữ liệu chi tiết message lấy từ users().messages().get(format="full").

    Returns:
        dict: Dictionary chứa thông tin chuẩn hóa của email.
    """
    payload = msg_detail.get("payload", {})
    headers_list = payload.get("headers", [])

    # Gom các header vào dictionary dạng chữ thường để tra cứu không phân biệt hoa thường
    headers = {h.get("name", "").lower(): h.get("value", "") for h in headers_list}

    # Bóc tách tên và email người gửi từ header From
    from_raw = headers.get("from", "")
    sender_name, sender_email = parseaddr(from_raw)
    if not sender_name:
        sender_name = sender_email

    # Lấy nội dung text và html
    body_text, body_html = decode_body(payload)

    labels = msg_detail.get("labelIds", [])

    return {
        "id": msg_detail.get("id", ""),
        "thread_id": msg_detail.get("threadId", ""),
        "sender_name": sender_name,
        "sender_email": sender_email,
        "recipient": headers.get("to", ""),
        "subject": headers.get("subject", "(Không có tiêu đề)"),
        "date": headers.get("date", ""),
        "snippet": msg_detail.get("snippet", ""),
        "body_text": body_text,
        "body_html": body_html,
        "is_unread": "UNREAD" in labels,
        "labels": labels,
    }


def fetch_recent_emails(service, max_results: int = 10) -> list[dict]:
    """
    Kéo danh sách email trong vòng 7 ngày gần nhất và bóc tách dữ liệu chuẩn.

    Args:
        service: Đối tượng Gmail API Resource đã xác thực.
        max_results (int): Số lượng email tối đa cần lấy (mặc định 10).

    Returns:
        list[dict]: Danh sách các dictionary email đã chuẩn hóa.
    """
    # Bước 1: Lấy danh sách ID email trong 7 ngày
    response = service.users().messages().list(
        userId="me",
        q="newer_than:7d",
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])
    emails = []

    # Bước 2 & 3: Lặp qua từng ID để lấy chi tiết định dạng full
    for msg in messages:
        msg_id = msg.get("id")
        msg_detail = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        # Bước 4: Chuẩn hóa dữ liệu qua hàm parse_email_message
        parsed_email = parse_email_message(msg_detail)
        emails.append(parsed_email)

    return emails


if __name__ == "__main__":
    from focus_email.auth import get_gmail_service

    print("Đang kiểm tra kết nối Gmail và kéo thử 2 email...")
    service = get_gmail_service()
    emails = fetch_recent_emails(service, max_results=2)
    print(f"Đã kéo thành công {len(emails)} email:")
    for email in emails:
        print(f"- [{email['sender_name']}] {email['subject']} ({email['date']})")