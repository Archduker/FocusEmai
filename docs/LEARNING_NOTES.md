# 📚 SỔ TAY ĐÚC KẾT KIẾN THỨC - FOCUSEMAIL PROJECT

Tài liệu này tổng hợp toàn bộ bản chất kiến thức bạn đã và đang học qua từng dòng code, chia làm 3 trụ cột: **Google Cloud & OAuth2**, **REST API** và **Kỹ năng lập trình Python chuyên sâu**.

---

## 🏛️ TRỤ CỘT 1: GOOGLE CLOUD & BẢO MẬT OAUTH 2.0

### 1. Vấn đề thực tế
* Khi viết một ứng dụng cần đọc email của chính bạn, bạn **tuyệt đối không được** lưu tài khoản & mật khẩu Gmail trong code (rất nguy hiểm và Google sẽ chặn ngay lập tức).
* **Giải pháp**: Cơ chế ủy quyền chuẩn quốc tế **OAuth 2.0** (Authorization Framework).

### 2. Sự khác biệt cốt lõi giữa `credentials.json` và `token.json`

| Tiêu chí | `credentials.json` (Thẻ Căn Cước của ỨNG DỤNG) | `token.json` (Chìa Khóa Ra Vào của NGƯỜI DÙNG) |
| :--- | :--- | :--- |
| **Nguồn gốc** | Tải từ Google Cloud Console về máy. | Do Google Server tự cấp sau khi bạn bấm "Cho phép" trên trình duyệt. |
| **Mục đích** | Nói với Google: *"Tôi là app FocusEmail do bạn BillTran tạo ra"*. | Nói với Google: *"Người dùng đã cấp quyền cho app này vào đọc hộp thư"*. |
| **Bao gồm gì?** | `client_id`, `client_secret`, `project_id`. | `access_token` (hết hạn sau 1h), `refresh_token` (vĩnh viễn). |
| **Tần suất dùng** | Chỉ dùng ở lần đầu tiên khi chưa có token. | Dùng liên tục ở mọi lần chạy sau. |

### 3. Cơ chế Refresh Token tự động ngầm
* `access_token` chỉ sống được 3600 giây (1 tiếng) vì lý do bảo mật.
* Khi hết 1 tiếng, code trong hàm `get_gmail_service()` kiểm tra:
  ```python
  if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
  ```
* Google kiểm tra `refresh_token`, thấy hợp lệ liền cấp ngay `access_token` mới trong 0.5 giây mà **không cần mở lại trình duyệt** làm phiền bạn.

### 4. Khái niệm Scopes (Phạm vi quyền hạn)
* Giống như thẻ từ ra vào tòa nhà: chỉ được vào sảnh hay được vào phòng tổng giám đốc.
* `gmail.readonly`: Chỉ được đọc email, không được làm gì khác.
* `gmail.modify`: Được đọc, xóa nhãn `UNREAD` (đánh dấu đã đọc), thêm nhãn cá nhân.

---

## 🌐 TRỤ CỘT 2: KIẾN THỨC VỀ REST API & BÓC TÁCH DỮ LIỆU EMAIL

### 1. API là gì trong dự án này?
* **Khái niệm**: API giống như người phục vụ bàn. 
  * Python script của bạn là Khách hàng.
  * Google Server là Nhà bếp.
  * API là Người phục vụ chuyển yêu cầu (Request) và bưng đĩa thức ăn (Response dạng JSON) về cho bạn.

### 2. Hai bước kéo dữ liệu tối ưu của Gmail API
Google thiết kế API theo 2 chặng để tiết kiệm băng thông mạng:
* **Chặng 1 - Lấy danh sách ID (`messages.list`)**:
  * Request: `service.users().messages().list(userId="me", q="newer_than:7d", maxResults=10)`
  * Google chỉ trả về danh sách ID nhẹ tênh: `[{"id": "18e6..."}, {"id": "18e7..."}]` (chưa có nội dung thư).
* **Chặng 2 - Lấy chi tiết từng thư (`messages.get`)**:
  * Request: `service.users().messages().get(userId="me", id=msg_id, format="full")`
  * Google trả về toàn bộ cây dữ liệu MIME khổng lồ của bức thư đó.

### 3. Cấu trúc cây dữ liệu MIME (Multipart Email)
Một email không phải là chuỗi text đơn giản, mà là một cái cây phân nhánh:
```text
Payload
├── Headers: [From, To, Subject, Date, ...]
└── Parts: (Danh sách các phần con)
    ├── Part 1 (mimeType: "text/plain"): Nội dung chữ thô
    └── Part 2 (mimeType: "text/html"): Nội dung trang trí đẹp mắt
```
* Đó là lý do trong `fetcher.py` bạn phải viết hàm đệ quy `extract_parts()` để duyệt qua tất cả các nhánh con của bức thư.

---

## 🐍 TRỤ CỘT 3: KỸ NĂNG & CÚ PHÁP PYTHON BẠN ĐÃ LÀM CHỦ

### 1. Quản lý gói hiện đại với `uv`
* Thay vì dùng `pip` và `venv` truyền thống chậm chạp, `uv` là công nghệ mới nhất viết bằng Rust:
  * `pyproject.toml`: Khai báo thư viện chuẩn PEP 621.
  * `uv run main.py`: Tự động tìm môi trường ảo, kích hoạt ngầm và chạy script.

### 2. Giải mã nhị phân (Binary Data) & Base64URL
* Dữ liệu email được Google mã hóa an toàn theo chuẩn URL-safe Base64.
* **Bẫy thiếu Padding**: Gmail thường bỏ các dấu `=` ở cuối chuỗi.
  ```python
  # Công thức toán bù đủ bội số của 4:
  padded_data = data + "=" * (-len(data) % 4)
  # Giải mã từ Base64 ra byte nhị phân:
  decoded_bytes = base64.urlsafe_b64decode(padded_data)
  # Giải mã byte sang chuỗi ký tự UTF-8 có dấu tiếng Việt:
  text_content = decoded_bytes.decode("utf-8", errors="ignore")
  ```

### 3. Bóc tách Header bằng thư viện chuẩn `email.utils.parseaddr`
* Header `From` thường có dạng: `"Medium Daily Digest <noreply@medium.com>"`.
* Thay vì viết regex phức tạp dễ sai, Python có sẵn hàm:
  ```python
  name, email = parseaddr("Medium Daily Digest <noreply@medium.com>")
  # Kết quả: name = "Medium Daily Digest", email = "noreply@medium.com"
  ```

### 4. Làm sạch mã HTML bằng `BeautifulSoup`
* Nếu email gửi dạng HTML phức tạp đầy thẻ tag `<div>`, `<span>`, CSS, bảng biểu:
  ```python
  soup = BeautifulSoup(body_html, "html.parser")
  body_text = soup.get_text(separator="\n")
  ```
  Hàm này tự động gạt bỏ toàn bộ mã code HTML và chỉ giữ lại văn bản thuần túy cho người đọc.

### 5. Kỹ thuật hàm lồng hàm (`Nested Function`) & từ khóa `nonlocal`
* Trong `decode_body()`, ta đặt hàm con `extract_parts()` bên trong:
  ```python
  def decode_body(payload):
      body_text = ""
      def extract_parts(part):
          nonlocal body_text # Cho phép hàm con sửa biến của hàm cha
          body_text += "..."
  ```

### 6. Kiến trúc phần mềm phân tầng (Layered Architecture)
* Không viết dồn 500 dòng code vào 1 file duy nhất.
* Chia thành các module độc lập:
  * `auth.py`: Tầng bảo mật (Security Layer).
  * `fetcher.py`: Tầng dữ liệu (Data Access Layer).
  * `main.py`: Tầng giao diện người dùng (Presentation Layer).

---

## 🎯 TEMPLATE TỰ ĐÁNH GIÁ (STAGE 1 & STAGE 2)

Bạn có thể copy đoạn này để tự trả lời và lưu lại:

```markdown
### 📝 BẢNG TỰ ĐÁNH GIÁ KIẾN THỨC BẢN THÂN

1. Về Google Cloud:
   - Tôi đã hiểu tại sao cần file `credentials.json` chưa? (Rồi / Chưa)
   - Tôi có biết tại sao lần 2 chạy không cần mở trình duyệt không? (Vì có token.json tự refresh ngầm)

2. Về REST API:
   - Tại sao Gmail API chia làm 2 hàm `list()` và `get()`? (Để tiết kiệm mạng, list chỉ lấy ID)
   - Vì sao phải đệ quy duyệt `parts`? (Vì email có cấu trúc cây MIME lồng nhau)

3. Về Python:
   - Cú pháp `base64.urlsafe_b64decode` dùng để làm gì? (Giải mã dữ liệu mã hóa của Google)
   - Hàm `parseaddr` giải quyết vấn đề gì? (Tách tên hiển thị và địa chỉ email)
   - Từ khóa `nonlocal` dùng khi nào? (Khi hàm con muốn gán giá trị cho biến ở hàm cha)
```
