from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import mysql.connector
from pydantic import ValidationError
from utils.datamodel import SignUpDataModel
from utils.token_verify_creator import token_creator


router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/user/") 
async def api_user_signup(request: Request, signup_data: SignUpDataModel):
    try:
        db_pool = request.state.db_pool.get("basic_db") 
        with db_pool.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT EXISTS(SELECT 1 FROM user_info WHERE email = %s);",(signup_data.email,)) 
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO `user_info` (username, password, email) VALUES (%s,%s,%s);",(signup_data.name,signup_data.password,signup_data.email,)) 
                    connection.commit()

                    cursor.execute("SELECT LAST_INSERT_ID();")
                    new_user_id = cursor.fetchone()[0]
                    input_data = {"id": new_user_id,'username':signup_data.name,'email':signup_data.email, 'password':signup_data.password}                                        
                    print('new user join: ',input_data)

                    access_token = token_creator(data=input_data)    
                    response = JSONResponse(status_code=200, content={"ok":True})
                    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")
                    return response             

                input_data = {"error": True,"message": "Invalid registration, duplicate email or other reasons"}
                return JSONResponse(status_code=400,content=input_data, headers=headers)
            
    except (mysql.connector.Error) as err:
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    except ValidationError as err:
        return JSONResponse(
            status_code=422,
            content={"error": True, "message": err.errors()}, # .errors()可以返回更仔細的資料
            headers=headers
        )      
    except (ValueError, Exception) as err:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": str(err)},
            headers=headers
        )
