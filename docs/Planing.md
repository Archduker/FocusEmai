# 📌 KẾ HOẠCH DỰ ÁN: FOCUSEMAIL AI (FULLSTACK & DOCKERIZED)

> **Mô hình kiến trúc tham chiếu**: Phỏng theo kiến trúc microservices hiện đại từ [8syncdev/ollama-docker-web-application](https://github.com/8syncdev/ollama-docker-web-application).
> Hệ thống tách biệt rõ ràng giữa Backend (FastAPI), Frontend (Next.js), Containerization (Docker Compose) và Module AI mở rộng (Ollama).

---

## 🎯 1. Mục Tiêu Lớn
1. **Làm chủ kiến trúc Fullstack hiện đại**: Backend Python (FastAPI) + Frontend React (Next.js 15 + TailwindCSS).
2. **Kỹ năng DevOps thực chiến**: Đóng gói toàn bộ ứng dụng bằng **Docker & Docker Compose** (chạy mọi nơi chỉ với 1 câu lệnh `docker compose up`).
3. **Làm chủ dữ liệu & API thực tế**: Kết nối Google Gmail API qua OAuth 2.0, xử lý MIME/Base64, quản lý dữ liệu với SQLite / Local Storage.
4. **Sẵn sàng tích hợp Local AI (Ollama)**: Dự phòng module LLM chạy offline trên máy để tự động tóm tắt email và trích xuất Action Item.

---

## 🛠️ 2. Tech Stack Chi Tiết

| Thành phần | Công nghệ | Vai trò & Mục đích |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI** (Python 3.11+ / 3.14) | Xử lý logic Gmail, OAuth2, bóc tách email, lưu trữ task, cung cấp RESTful API, tự động sinh tài liệu `/docs` (Swagger UI). Quản lý qua `uv`. |
| **Frontend UI** | **Next.js 15+** (React + TailwindCSS) | Giao diện Focus Checklist & Kanban Board mượt mà, tối ưu SEO & UX, gọi API Backend qua fetch/SWR. *(Lưu ý: Next.js cho FE, không phải NestJS là BE Node)*. |
| **Database** | **SQLite** / SQLModel | Lưu trữ cục bộ trạng thái task (`TODO`, `IN_PROGRESS`, `DONE`), ghi chú, và cache email mà không phụ thuộc cloud database. |
| **DevOps** | **Docker** & **Docker Compose** | Đóng gói môi trường tách biệt: container `backend`, container `frontend`, và container `ollama-server`. |
| **AI / LLM (Upgrade)** | **Ollama** (Qwen 2.5 / Llama 3.2) | Mô hình ngôn ngữ chạy local: Tóm tắt nội dung email dài, tự động phân loại mức độ khẩn cấp, chat hỏi đáp về hộp thư. |

---

## 🏗️ 3. Sơ Đồ Kiến Trúc Hệ Thống (Architecture)

```mermaid
flowchart TD
    User["👤 Người Dùng Trình Duyệt"] -->|Truy cập Port 3000| FE["🌐 Frontend (Next.js 15 + TailwindCSS)"]
    FE -->|REST API Request /api/... Port 8000| BE["⚡ Backend (FastAPI)"]
    
    subgraph Docker Network ["🐳 Docker Compose Network"]
        FE
        BE
        DB[("💾 SQLite Database")]
        OLLAMA["🤖 Ollama LLM Container (Port 11434)\n(Qwen / Llama)"]
    end

    BE -->|Query & Save Tasks| DB
    BE -->|OAuth 2.0 / REST API| GMAIL["☁️ Google Gmail API"]
    BE -.->|Gọi tóm tắt / trích xuất Task (Bản nâng cấp)| OLLAMA
```

### 📁 Cấu trúc thư mục dự kiến (Monorepo)
```text
EmailTool/
├── docker-compose.yml              # Quản lý khởi chạy đồng thời các service
├── Planing.md                      # Lộ trình học tập & kế hoạch
├── LEARNING_NOTES.md               # Sổ tay kiến thức đúc kết
├── API_SPECIFICATION.md            # Thiết kế chuẩn API & Models
├── backend/                        # ⚡ FastAPI Service
│   ├── Dockerfile
│   ├── pyproject.toml              # Quản lý bởi uv
│   ├── main.py                     # Entry point FastAPI app
│   ├── credentials.json            # Google OAuth App ID
│   ├── token.json                  # User Token (tự sinh)
│   └── src/focus_email/
│       ├── auth.py                 # OAuth 2.0 handler
│       ├── fetcher.py              # Gmail API fetcher & decoder
│       ├── models.py               # Data models (Pydantic / Dataclass)
│       ├── storage.py              # SQLite / JSON task storage
│       └── routers/                # API Endpoints (tasks, emails, sync)
├── frontend/                       # 🌐 Next.js 15 Service
│   ├── Dockerfile
│   ├── package.json
│   ├── app/                        # App Router (Checklist & Kanban pages)
│   ├── components/                 # TaskCard, EmailViewer, FilterBar
│   └── tailwind.config.ts
└── ollama/                         # 🤖 Ollama Service (Bản nâng cấp AI)
    ├── Dockerfile
    └── pull-model.sh               # Tải model (Qwen/Llama)
```

---

## 🗺️ 4. Lộ Trình 5 Stages Chi Tiết (Đã Nâng Cấp)

### 📍 Stage 1: Xác Thực OAuth2 & Kéo Dữ Liệu Email Thô (CLI) ✅ [HOÀN THÀNH]
* **Mục tiêu**: Làm chủ kết nối Gmail REST API, xác thực OAuth2 an toàn, bóc tách cấu trúc MIME và Base64URL.
* **Kết quả**: Đã test thành công với tài khoản Gmail thật, lấy đầy đủ Sender, Subject, Date, Body text/HTML.

---

### 📍 Stage 2: Xây Dựng Backend FastAPI & Chuẩn Hóa RESTful API
* **Mục tiêu**: Đưa toàn bộ logic Stage 1 vào framework **FastAPI**, mô hình hóa dữ liệu bằng **Pydantic** và lưu trữ trạng thái Task vào **SQLite / Local Storage**.
* **Các bước (Steps)**:
  * **Step 1**: Cấu trúc lại thư mục Backend (`backend/`), cài đặt FastAPI & Uvicorn qua `uv`.
  * **Step 2**: Định nghĩa Pydantic Models (`EmailMessage`, `EmailTask`) kế thừa từ thiết kế chuẩn.
  * **Step 3**: Viết module lưu trữ `storage.py` (lưu trạng thái `TODO`, `IN_PROGRESS`, `DONE`, `priority`, `notes`).
  * **Step 4**: Xây dựng các REST Endpoints:
    * `GET /api/status`: Kiểm tra trạng thái Google Auth.
    * `GET /api/tasks`: Lấy danh sách task (kèm filter trạng thái).
    * `PATCH /api/tasks/{task_id}`: Cập nhật trạng thái / ghi chú task.
    * `POST /api/sync`: Kéo email mới và đồng bộ trạng thái về Gmail thật.
* **Test Gate**: Truy cập `http://localhost:8000/docs` (Swagger UI), test trực tiếp các endpoint trả về dữ liệu chuẩn JSON.
* **Tự đánh giá**: Điền Template Stage 2.

---

### 📍 Stage 3: Xây Dựng Giao Diện Hiện Đại Với Next.js 15 + TailwindCSS
* **Mục tiêu**: Xây dựng Frontend tách biệt bằng **Next.js (App Router)** với giao diện Focus Checklist và Kanban Board trực quan, thẩm mỹ cao.
* **Các bước (Steps)**:
  * **Step 1**: Khởi tạo project `frontend/` bằng `create-next-app` với Next.js 15, TypeScript & TailwindCSS.
  * **Step 2**: Xây dựng giao diện **Focus Checklist**: Checkbox hoàn thành, thẻ email gọn gàng, modal/drawer xem chi tiết toàn văn email (HTML/Text).
  * **Step 3**: Xây dựng giao diện **Kanban Board**: Phân cột `TODO` | `IN_PROGRESS` | `DONE`.
  * **Step 4**: Kết nối API Client: Gọi backend FastAPI (`http://localhost:8000`), cập nhật trạng thái UI tức thì (Optimistic UI update).
* **Test Gate**: Giao diện chạy mượt trên `http://localhost:3000`, thao tác tick task hoặc kéo thả cập nhật ngay vào SQLite Backend.
* **Tự đánh giá**: Điền Template Stage 3.

---

### 📍 Stage 4: Đóng Gói Toàn Hệ Thống Bằng Docker & Docker Compose
* **Mục tiêu**: Đóng gói Frontend và Backend vào các container độc lập, thiết lập mạng nội bộ để ứng dụng chạy độc lập trên bất kỳ máy tính nào.
* **Các bước (Steps)**:
  * **Step 1**: Viết `backend/Dockerfile` (dùng base Python slim, cài đặt tối ưu với `uv`).
  * **Step 2**: Viết `frontend/Dockerfile` (Multi-stage build cho Next.js để image siêu nhẹ).
  * **Step 3**: Viết `docker-compose.yml` liên kết Backend (Port 8000) và Frontend (Port 3000), cấu hình volumes cho token và SQLite database.
* **Test Gate**: Chỉ cần chạy lệnh `docker compose up --build`, mở trình duyệt truy cập app mượt mà.
* **Tự đánh giá**: Điền Template Stage 4.

---

### 📍 Stage 5: Nâng Cấp Tích Hợp AI Agent Với Ollama (Bản Nâng Cấp)
* **Mục tiêu**: Tích hợp container **Ollama** chạy mô hình ngôn ngữ mã nguồn mở (Qwen 2.5 hoặc Llama 3.2) để thông minh hóa hòm thư.
* **Các bước (Steps)**:
  * **Step 1**: Thêm service `ollama-server` vào `docker-compose.yml` với kịch bản tải model tự động.
  * **Step 2**: Viết module AI Client trong FastAPI (`ai_agent.py`) kết nối tới Ollama API (`http://ollama-server:11434`).
  * **Step 3**: Tạo các tính năng thông minh:
    * **Email Summarizer**: Tóm tắt email dài thành 3 gạch đầu dòng ngắn gọn.
    * **Action Item Extractor**: Tự động phát hiện deadline và việc cần làm từ email để điền sẵn vào Task.
    * **Email Chatbot**: Hộp chat bên cạnh email cho phép hỏi: *"Email này yêu cầu tôi làm gì trước ngày mai?"*.
  * **Step 4**: Bổ sung UI trên Next.js để kích hoạt và hiển thị phản hồi từ AI.
* **Test Gate**: Bấm nút "Tóm tắt với AI" trên 1 email bất kỳ, hệ thống phản hồi tóm tắt chuẩn xác mà không tốn phí API bên ngoài.
* **Tự đánh giá**: Tổng kết toàn bộ dự án.

---

## 📝 5. Template Báo Cáo Đúc Kết Cuối Mỗi Stage
```markdown
# 📝 BÁO CÁO ĐÚC KẾT KIẾN THỨC - STAGE [Số]: [Tên Stage]

### 1. 🎯 Mục tiêu của Stage này
- Mục tiêu lý thuyết: ...
- Mục tiêu sản phẩm: ...

### 2. 🧠 Những khái niệm / công nghệ mới mình đã học được
- Khái niệm: ...
- Cú pháp / Kỹ thuật mới (FastAPI, Next.js, Docker, Ollama): ...

### 3. 💻 Mức độ tự tay viết code
- Phần tự tay viết được: ...
- Phần được hướng dẫn và hiểu bản chất: ...

### 4. 🐞 Lỗi (Bug) gặp phải & Cách giải quyết
- Lỗi: ... -> Cách sửa: ...

### 5. 🧪 Kết quả Test thử nghiệm
- [x] Đạt test case: ...

### 6. ⭐ Điểm tự đánh giá mức độ hiểu bài (1 - 10): .../10
```