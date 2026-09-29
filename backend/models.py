"""
Data Models cho FocusEmail
sử dụng pydantic v2 đẻ định nghãi cấu trúc dữ liệu chuẩn cho FastAPI & Frontend
"""

from enum import Enum
from typing import Optional 
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    """Trạnh thái của Email"""
    TODO = 'TODO'
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"

class TaskPriority(str, Enum):
    """Mực độ ưu tiên của email"""
    LOW = 'LOW'
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"

class EmailMessage(BaseModel):
    """Thông tin của Email được chuẩn hóa từ gmail API"""
    id: str = Field (..., description = "id duy nhất của email", index = True)
    thread_id = str = Field(..., description = " ID chuỗi hội thoại")                                                                                                        
    sender_name: str = Field(..., description="Tên hiển thị người gửi")                                                                                                  
    sender_email: str = Field(..., description="Địa chỉ email người gửi")                                                                                                
    recipient: str = Field(..., description="Địa chỉ email người nhận")                                                                                                  
    subject: str = Field(..., description="Tiêu đề email")                                                                                                               
    date: str = Field(..., description="Thời gian gửi đã chuẩn hóa")                                                                                                     
    snippet: str = Field("", description="Đoạn trích ngắn tóm tắt nội dung")                                                                                             
    body_text: str = Field("", description="Nội dung chữ thuần (Plain text)")                                                                                            
    body_html: str = Field("", description="Nội dung định dạng HTML")                                                                                                    
    is_unread: bool = Field(False, description="Email chưa đọc (True) hay đã đọc (False)")                                                                               
    labels: list[str] = Field(default_factory=list, description="Danh sách nhãn của email")                                                                              
                                                                                                                                                                             
                                                                                                                                                                             
class EmailTask(BaseModel):                                                                                                                                              
        """Mô hình công việc gắn liền với một email (dùng cho Checklist & Kanban)."""                                                                                        
        task_id: str = Field(..., description="ID của task (mặc định lấy trùng với email.id)")                                                                               
        email: EmailMessage = Field(..., description="Dữ liệu chi tiết của email")                                                                                           
        status: TaskStatus = Field(default=TaskStatus.TODO, description="Trạng thái công việc")                                                                              
        priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Mức độ ưu tiên")                                                                            
        notes: Optional[str] = Field(default=None, description="Ghi chú cá nhân thêm vào task")                                                                              
        due_date: Optional[str] = Field(default=None, description="Hạn chót xử lý (YYYY-MM-DD)")                                                                             
        created_at: str = Field(..., description="Thời điểm tạo task (ISO 8601)")                                                                                            
        updated_at: str = Field(..., description="Thời điểm cập nhật trạng thái gần nhất")                                                                                   
                                                                                                                                                                             
                                                                                                                                                                             
class TaskUpdate(BaseModel):                                                                                                                                             
        """Dữ liệu gửi từ Frontend khi cập nhật trạng thái hoặc ghi chú của task."""                                                                                         
        status: Optional[TaskStatus] = Field(default=None, description="Trạng thái mới")                                                                                     
        priority: Optional[TaskPriority] = Field(default=None, description="Độ ưu tiên mới")                                                                                 
        notes: Optional[str] = Field(default=None, description="Ghi chú mới")                                                                                                
        due_date: Optional[str] = Field(default=None, description="Hạn chót mới")                                                                                            
                                                                                                                                                                             
                                                                                                                                                                             
class AuthStatusResponse(BaseModel):                                                                                                                                     
        """Thông tin trạng thái đăng nhập tài khoản Google."""                                                                                                               
        authenticated: bool                                                                                                                                                  
        user_email: Optional[str] = None                                                                                                                                     
                                                                                                                                                                             
                                                                                                                                                                             
class TaskListResponse(BaseModel):                                                                                                                                       
        """Danh sách các task trả về cho giao diện."""                                                                                                                       
        total: int                                                                                                                                                           
        tasks: list[EmailTask]                                                                                                                                                                  