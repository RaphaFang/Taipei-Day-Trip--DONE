from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/user/logout")
async def logout(request: Request):
    try:
        response = JSONResponse(status_code=200, content={"message": "Logged out successfully"})
        response.delete_cookie(key="access_token")
        return response
    except (ValueError, Exception) as err:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": str(err)},
            headers=headers
        )