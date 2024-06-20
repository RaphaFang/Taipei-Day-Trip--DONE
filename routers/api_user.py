from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
import mysql.connector
from pydantic import ValidationError
from utils.datamodel import SignUpDataModel

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/user") # data: SignUpDataModel = Depends() 這方式得不到資料
async def api_user_signup(request: Request, signup_data: SignUpDataModel):
    try:
        db_pool = request.state.db_pool.get("basic_db") 
        with db_pool.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT EXISTS(SELECT 1 FROM user_info WHERE email = %s);",(signup_data.email,)) 
                repeat_TF = cursor.fetchall()[0][0]

                if repeat_TF!=1:
                    cursor.execute("INSERT INTO `user_info` (username, password, email) VALUES (%s,%s,%s);",(signup_data.name,signup_data.password,signup_data.email,)) 
                    connection.commit()
                    input_data = { "ok": True }
                    return JSONResponse(status_code=200,content=input_data, headers=headers)

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
