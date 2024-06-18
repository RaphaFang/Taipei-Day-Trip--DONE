from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import JSONResponse
import mysql.connector
from token_verify_creator import token_verifier
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/api/user/auth")
async def api_user_get(request: Request,token: str = Depends(oauth2_scheme)):
    token_output = token_verifier(token)
    try:
        db_pool = request.state.db_pool.get("basic_db") 
        with db_pool.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(" SELECT EXISTS ( SELECT 1 FROM user_info WHERE id = %s AND email = %s AND password = %s) AS api_user_get;", (token_output['id'],token_output['email'],token_output['password'])) 
                data = cursor.fetchone()['api_user_get']
                if data!=0:
                    input_data = {"data": {"id": token_output['id'],'name':token_output['username'],'email':token_output['email']}}                                        
                    print(input_data)
                    return JSONResponse(status_code=200,content=input_data, headers=headers)
                else:
                    input_data = {"data": None}
                    return JSONResponse(status_code=200,content=input_data, headers=headers)

    except (mysql.connector.Error, ValueError, Exception) as err:
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )