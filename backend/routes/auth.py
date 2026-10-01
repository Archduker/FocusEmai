import os 
from fastapi import APIRouter
from src.focus_email.models import AuthStatusResponse
from src.focus_email.auth import _resolve_path 

router = APIRouter(tags=["Auth"])

@router.get("/api/status",response_model = AuthStatusResponse)
def get_auth_status():
    """Kiểm tra trạng thái đăng nhập Gmail OAuth2"""
    token_file = _resolve_path("token.json")
    has_token = os.path.exixts(tonken_file)
    return AuthStatusRespons(
        authennticated = has_token, 
        user_email = "t20067771@gmail.com" if has_token else None,
    )

