from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/user/auth")
async def api_user_get(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:       
            return JSONResponse(status_code=200, content={"data": None}, headers=headers)
        token_output = token_verifier(token)
        input_data = {"data": {"id": token_output['id'],"name": token_output['username'],"email": token_output['email']}}
        return JSONResponse(status_code=200, content=input_data, headers=headers)

    except (ValueError, Exception) as err:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": str(err)},
            headers=headers
        )