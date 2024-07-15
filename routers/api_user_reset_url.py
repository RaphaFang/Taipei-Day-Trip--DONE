from fastapi import APIRouter, Request, Form, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse
from utils.token_verify_creator import token_verifier, token_creator
from datetime import timedelta

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/user/reset_url_verify")
async def reset_password(request: Request, token: str, bt:BackgroundTasks): 
    try:
        token_output = token_verifier(token)
        if isinstance(token_output, JSONResponse):
            return RedirectResponse(url=f"/?reset_password_token_status=error&message=Invalid+access+to+resetting+password.")
        if isinstance(token_output, dict):
            input_data = {"id": token_output['id'],'username':token_output['username'],'email':token_output['email'], 'password':token_output['password']}                                        
            access_token = token_creator(data=input_data)
            response = RedirectResponse(url="/?reset_password_token_status=success")
            response.set_cookie(key="15min_token", value=access_token, httponly=True, secure=True, samesite="Strict",expires=timedelta(minutes=15).total_seconds())
            return response
            # 前端檢測這串url代碼，如果是success，才可以跳出修改密碼的彈窗
            # 前端檢測cookie，如果有才可以讓他修改，並且這cookie的期限很短
     
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)