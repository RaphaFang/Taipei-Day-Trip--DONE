from fastapi import APIRouter, Request, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
import redis
import json
import aiomysql
import redis.asyncio as aioredis 


router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/user/logout")
async def logout(request: Request, bt:BackgroundTasks):  # request: Request 刪除不需要。request.cookies.get("access_token") 所以直接response
    try:
        token = request.cookies.get("access_token")
        token_response = token_verifier(token)
        if isinstance(token_response, JSONResponse):
            return token_response
        token_output = token_response

        if token_output:

            async def delete_user_r(request, id):
                redis_pool = request.state.async_redis_pool
                async with aioredis.Redis(connection_pool=redis_pool) as r:
                    b = await r.get(f"user:{id}:booking")
                    await r.delete(f"user:{id}:booking")
                    await r.delete(f"user:{id}:booking_trigger_key")
                    return b
            redis_data = await delete_user_r(request,token_output['id'])

            async def redis_to_sql(request,b):
                sql_pool = request.state.async_sql_pool 
                async with sql_pool.acquire() as connection:
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        if b:
                            b = json.loads(b)
                            await cursor.execute("""
                                INSERT INTO user_booking_tentative (
                                    creator_id, attraction_id, name, address, image, date, time, price
                                )
                                SELECT %s, %s, %s, %s, %s, %s, %s, %s
                                ON DUPLICATE KEY UPDATE
                                    attraction_id = VALUES(attraction_id), name = VALUES(name), address = VALUES(address), image = VALUES(image), date = VALUES(date), time = VALUES(time), price = VALUES(price);
                            """, (token_output['id'], b['attraction_id'], b['name'], b['address'], b['image'], b['date'], b['time'], b['price']))
                        else:
                            print('User logout, with nothing to add to sql. Cleaning up sql...')
                            await cursor.execute("DELETE FROM user_booking_tentative WHERE creator_id = %s;", (token_output['id'],))
                        await connection.commit()
            bt.add_task(redis_to_sql, request, redis_data)

            response = JSONResponse(status_code=200, content={"message": "Logged out successfully"})
            response.delete_cookie(key="access_token")
            return response
        
        else:
            content_data = {"error": True, "message": "Token verification failed"}
            return JSONResponse(status_code=403, content=content_data, headers=headers)
 
    except (aiomysql.Error, redis.RedisError) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)