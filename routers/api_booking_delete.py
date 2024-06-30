from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import mysql.connector
from utils.token_verify_creator import token_verifier

import redis

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.delete("/api/booking")
async def api_booking_delete(request: Request): 
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "Please log-in to access the booking page."}
            return JSONResponse(status_code=403,content=content_data, headers=headers)
        
        token_output = token_verifier(token)
        if token_output:
            # sql_pool = request.state.sql_db_pool.get("default") 
            # with sql_pool.get_connection() as connection:
            #     with connection.cursor(dictionary=True) as cursor:
            #         cursor.execute("""
            #             DELETE FROM user_booking_tentative WHERE creator_id = %s;""", (token_output['id'],))
            #         connection.commit()
            #         print('sql delete')
            #         if b == None:
                        
            redis_pool = request.state.redis_db_pool.get("default")
            r = redis.Redis(connection_pool=redis_pool)
            redis_key = f"user:{token_output['id']}:booking"
            r.delete(redis_key)
            print('redis delete')

            content_data = {"ok": True}
            return JSONResponse(content=content_data, headers=headers)           

    except (redis.RedisError) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)