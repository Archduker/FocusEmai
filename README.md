# 📬 FocusEmail AI

Hệ thống quản lý hộp thư tập trung, biến email thành danh sách công việc (Task Checklist & Kanban) tích hợp trí tuệ nhân tạo (Local LLM qua Ollama).

---

## 🏛️ Kiến Trúc Hệ Thống (Architecture)

Dự án được xây dựng theo kiến trúc Microservices đóng gói bằng Docker:
- **`backend/`**: RESTful API xây dựng bằng **FastAPI** (Python 3.11+ / 3.14, quản lý bởi `uv`). Xử lý Google OAuth2, Gmail API và lưu trữ SQLite.
- **`frontend/`**: Giao diện người dùng hiện đại xây dựng bằng **Next.js 15+** (React + TailwindCSS).
- **`ollama/`**: Module AI Agent chạy local (Qwen 2.5 / Llama 3.2) phục vụ tóm tắt thư và gợi ý hành động.
- **`docs/`**: Tài liệu thiết kế, sổ tay kiến thức và lộ trình dự án.

---

## 📚 Tài Liệu Dự Án (Documentation)

- [Kế hoạch & Lộ trình 5 Stages](file:///home/billtran/Desktop/EmailTool/docs/Planing.md)
- [Sổ tay đúc kết kiến thức (Learning Notes)](file:///home/billtran/Desktop/EmailTool/docs/LEARNING_NOTES.md)
- [Đặc tả kỹ thuật API & Data Models](file:///home/billtran/Desktop/EmailTool/docs/API_SPECIFICATION.md)
- [Báo cáo hoàn thành Stage 1](file:///home/billtran/Desktop/EmailTool/docs/stage1.md)

---

## ⚡ Hướng Dẫn Chạy Thử Backend (Stage 1 & 2)

```bash
cd backend
uv run main.py
```
