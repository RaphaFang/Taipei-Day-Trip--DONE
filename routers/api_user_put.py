from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import mysql.connector
from utils.token_verify_creator import token_creator
from utils.datamodel import SignInDataModel
from pydantic import ValidationError
import redis
import json

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.put("/api/user/auth")
async def api_user_put(request: Request, login_data: SignInDataModel):
    try:
        sql_pool = request.state.sql_db_pool.get("default") 
        with sql_pool.get_connection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_info WHERE email = %s AND password = %s;", (login_data.email,login_data.password,)) 
                data = cursor.fetchone()

                if data:
                    input_data = {"id": data['id'],'username':data['username'],'email':data['email'], 'password':data['password']}                                        
                    access_token = token_creator(data=input_data)

                    cursor.execute("SELECT * FROM user_booking_tentative WHERE creator_id = %s;", (data['id'],)) 
                    last_d = cursor.fetchone()

                    if last_d:
                        redis_pool = request.state.redis_db_pool.get("default") 
                        r = redis.Redis(connection_pool=redis_pool)
                        booking_data = {
                            "attraction_id": last_d['attraction_id'],
                            "name": last_d['name'],
                            "address": last_d['address'],
                            "image": last_d['image'],
                            "date": last_d['date'].strftime("%Y-%m-%d"),
                            "time": last_d['time'],
                            "price":  str(last_d['price']) 
                        }
                        r.set(f"user:{data['id']}:booking", json.dumps(booking_data))

                    response = JSONResponse(status_code=200, content={"message": "Login successful"})
                    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")
                    return response
                return JSONResponse(status_code=400,content={"error": True, "message": 'Invalid user info, please make sure the email and password are correct.'}, headers=headers)

    except (mysql.connector.Error, redis.RedisError) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except ValidationError as err:
        return JSONResponse(status_code=422,content={"error": True, "message": err.errors()},headers=headers)     
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)