from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from utils.token_verify_creator import token_verifier
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/api/user/auth")
async def api_user_get(request: Request,token: str = Depends(oauth2_scheme)):
    # 目前這作法，除了檢查token，也檢查了token跟SQL的資訊，但是可能非必要
    try:
        token_output = token_verifier(token)
        print(token_output)

        db_pool = request.state.db_pool.get("basic_db") 
        with db_pool.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:

                cursor.execute("SELECT id, username, email FROM user_info WHERE id = %s AND email = %s;", (token_output['id'], token_output['email']))
                user = cursor.fetchone()
                if user:
                    input_data = {"data": {"id":user['id'],'name':user['username'],'email':user['email']}}                                        
                    return JSONResponse(status_code=200,content=input_data, headers=headers)
                else:
                    input_data = {"data": None}
                    return JSONResponse(status_code=200,content=input_data, headers=headers)
  
    except HTTPException as http_err:
        return JSONResponse(
            status_code=http_err.status_code,
            content={"error": True, "message": http_err.detail},
            headers=http_err.headers
        )
    except (mysql.connector.Error) as err:
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    except (ValueError, Exception) as err:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": str(err)},
            headers=headers
        )