# 📝 BÁO CÁO ĐÚC KẾT KIẾN THỨC - STAGE 2

### 1. 🎯 Mục tiêu của Stage này

- Đưa Gmail CLI thành FastAPI backend có Swagger tại `/docs`.
- Chuẩn hóa email/task bằng Pydantic và giữ trạng thái task cục bộ qua `tasks.json`.

### 2. 🧠 Những khái niệm / công nghệ mới đã áp dụng

- FastAPI router, CORS, query/path parameter, response model và `HTTPException`.
- Pydantic enum/model để xác thực request và sinh OpenAPI schema.
- Layered architecture: route → controller → storage.
- JSON atomic write và smart merge theo Gmail message ID.

### 3. 💻 Hạng mục đã hoàn thành

- [x] `TaskStorage`: load/save, lọc, tìm, PATCH và merge email không ghi đè task cũ.
- [x] Controllers cho task và sync Gmail.
- [x] `GET /api/status`, `GET /api/tasks`, `GET /api/tasks/{task_id}`, `PATCH /api/tasks/{task_id}`, `POST /api/sync`.
- [x] Đăng ký router, CORS và health check trong `app.py`.
- [x] Test storage, route handlers và OpenAPI độc lập bằng thư mục tạm.

### 4. 🐞 Lỗi đã phát hiện và cách xử lý

- Router ban đầu dùng `fastapt`, sai tên model, sai `os.path.exists`, tên file `__inti__.py`/`task.py` không khớp tài liệu, và không có phần thân endpoint. Đã thay bằng router hợp lệ `routes/tasks.py`, `routes/__init__.py` và handlers hoàn chỉnh.
- `fetch_recent_emails` không nhận số ngày, trong khi flow sync yêu cầu 7 ngày. Đã thêm `days_back` để query Gmail được cấu hình rõ ràng.

### 5. 🧪 Kết quả test thử nghiệm

- [x] Biên dịch toàn bộ backend.
- [x] Kiểm tra app đăng ký đủ routes.
- [x] Test smart merge bảo toàn `DONE` và `notes`.
- [x] Test filter, PATCH, đọc task chi tiết và `404`.

### 6. ⭐ Tự đánh giá

`8/10`: Đã có backend Stage 2 chạy độc lập và test được. Bước tiếp theo hợp lý là Stage 3 frontend gọi các endpoint này.
