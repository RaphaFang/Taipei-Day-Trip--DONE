from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
import mysql.connector
import os
import jwt
from datetime import datetime, timedelta

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

ALGORITHM = "RS256"
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(days=7)})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/api/user/auth")
async def api_user(request: Request, signin_email: str = Form(...), signin_password: str= Form(...)):
    try:
        db_pool = request.state.db_pool.get("basic_db") 
        with db_pool.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_info WHERE email = %s AND password = %s;", (signin_email,signin_password,)) 
                data = cursor.fetchone()

                if data:
                    input_data = {"id": data['id'],'username':data['username'],'email':data['email'], 'password':data['password']}                                        
                    access_token = create_access_token(data=input_data)    
                    print(input_data)
                    print(access_token)                
                    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, headers=headers)
                else:
                    print('aaa')
                    return JSONResponse(status_code=400,content={"error": True, "message": 'Incorrect sign-in info'}, headers=headers)

    
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    except ValueError as err:
        return JSONResponse(    
            status_code=400,
            content={"error": True, "message": str(err)},
            headers=headers
        )
