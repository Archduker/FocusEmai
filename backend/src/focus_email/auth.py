import os.path
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Thư mục gốc của backend (nơi chứa credentials.json và token.json)
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

# Quyền truy cập Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _resolve_path(path_str: str) -> str:
    """Tự động tìm đường dẫn file dù chạy từ thư mục gốc hay thư mục backend/."""
    p = Path(path_str)
    if p.is_absolute():
        return str(p)
    if p.exists():
        return str(p.resolve())
    candidate = BACKEND_DIR / path_str
    if candidate.exists():
        return str(candidate)
    return str(candidate)


def get_gmail_service(credentials_path="credentials.json", token_path="token.json"):
    """
    Khởi tạo và trả về đối tượng Gmail API service sau khi xác thực OAuth 2.0.

    Xử lý 3 trạng thái:
    1. Đã có token.json hợp lệ -> Nạp trực tiếp.
    2. token.json hết hạn nhưng có refresh_token -> Tự động gia hạn ngầm.
    3. Chưa có token.json -> Đọc credentials.json, mở trình duyệt để người dùng đăng nhập và lưu token.json.

    Args:
        credentials_path (str): Đường dẫn đến file credentials.json tải từ Google Cloud.
        token_path (str): Đường dẫn lưu file token.json sau khi xác thực.

    Returns:
        googleapiclient.discovery.Resource: Đối tượng service để thao tác với Gmail API.
    """
    credentials_path = _resolve_path(credentials_path)
    token_path = _resolve_path(token_path)
    creds = None

    # Trạng thái 1: Nạp token đã lưu từ trước
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Trạng thái 2 & 3: Nếu chưa có token hoặc token không còn hợp lệ
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Tự động gia hạn ngầm (Refresh Token flow)
            creds.refresh(Request())
        else:
            # Lần đầu đăng nhập: cần file credentials.json
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Không tìm thấy file '{credentials_path}'. "
                    "Vui lòng tải credentials.json từ Google Cloud Console và đặt vào thư mục dự án."
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Lưu lại token vào file để các lần chạy sau không cần mở trình duyệt
        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    # Khởi tạo đối tượng service Gmail API v1
    service = build("gmail", "v1", credentials=creds)
    return service


if __name__ == "__main__":
    service = get_gmail_service()
    print(" Gmail service đã được khởi tạo thành công!")
