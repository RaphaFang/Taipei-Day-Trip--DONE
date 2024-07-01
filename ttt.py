from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
import mysql.connector
from utils.token_verify_creator import token_verifier
import redis
import json
import asyncio

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/user/logout")
async def logout(request: Request):  
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "You did not get the token in cookies, how did you even come to the log-out step???"}
            return JSONResponse(status_code=403, content=content_data, headers=headers)
        
        token_output = token_verifier(token)
        if token_output:
            redis_pool = request.state.redis_db_pool.get("default") 
            r = redis.Redis(connection_pool=redis_pool)
            b = r.get(f"user:{token_output['id']}:booking")

            sql_pool = request.state.sql_db_pool.get("default") 

            async def db_task():
                with sql_pool.get_connection() as connection:
                    with connection.cursor(dictionary=True) as cursor:
                        if b:
                            b = json.loads(b)
                            cursor.execute("""
                                INSERT INTO user_booking_tentative (
                                    creator_id, attraction_id, name, address, image, date, time, price
                                )
                                SELECT %s, %s, %s, %s, %s, %s, %s, %s
                                ON DUPLICATE KEY UPDATE
                                    attraction_id = VALUES(attraction_id), name = VALUES(name), address = VALUES(address), image = VALUES(image), date = VALUES(date), time = VALUES(time), price = VALUES(price);
                            """, (token_output['id'], b['attraction_id'], b['name'], b['address'], b['image'], b['date'], b['time'], b['price']))
                            connection.commit()
                        else:
                            print('User logout, with nothing to add to sql. Cleaning up sql...')
                            cursor.execute("DELETE FROM user_booking_tentative WHERE creator_id = %s;", (token_output['id'],))
                            connection.commit()

            await asyncio.get_event_loop().run_in_executor(None, db_task)

            redis_key = f"user:{token_output['id']}:booking"
            r.delete(redis_key)

            response = JSONResponse(status_code=200, content={"message": "Logged out successfully"})
            response.delete_cookie(key="access_token")
            return response
        
        else:
            content_data = {"error": True, "message": "Token verification failed"}
            return JSONResponse(status_code=403, content=content_data, headers=headers)
 
    except (mysql.connector.Error, redis.RedisError) as err:
        return JSONResponse(status_code=500, content={"error": True, "message": str(err)}, headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400, content={"error": True, "message": str(err)}, headers=headers)
