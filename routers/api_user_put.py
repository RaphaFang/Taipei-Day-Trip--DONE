from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_creator
from utils.datamodel import SignInDataModel
from pydantic import ValidationError
import redis
import json
import aiomysql 
import redis.asyncio as aioredis 

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.put("/api/user/auth")
async def api_user_put(request: Request, login_data: SignInDataModel,bt:BackgroundTasks):
    try:
        async def search_user_login(request,e,p):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("SELECT * FROM user_info WHERE email = %s AND password = %s;", (e,p,)) 
                    data =  await cursor.fetchone()
                    if data:
                        input_data = {"id": data['id'],'username':data['username'],'email':data['email'], 'password':data['password']}                                        
                        access_token = token_creator(data=input_data)

                        await cursor.execute("SELECT * FROM user_booking_tentative WHERE creator_id = %s;", (data['id'],)) 
                        last_d = await cursor.fetchone()

                        # await cursor.execute("SELECT * FROM user_booking_finalized WHERE creator_id = %s AND given_status = 'PAID' ORDER BY created_at LIMIT 10;", (data['id'],))
                        # history_d = await cursor.fetchall()

                        return access_token, last_d
                    else:
                        return JSONResponse(status_code=400,content={"error": True, "message": 'Invalid user info, please make sure the email and password are correct.'}, headers=headers)

        async def booking_data_r(request, last_d):
            redis_pool = request.state.async_redis_pool
            async with aioredis.Redis(connection_pool=redis_pool) as r:
                if last_d:
                        booking_data = {
                        "attraction_id": last_d['attraction_id'],
                        "name": last_d['name'],
                        "address": last_d['address'],
                        "image": last_d['image'],
                        "date": last_d['date'].strftime("%Y-%m-%d"),
                        "time": last_d['time'],
                        "price": str(last_d['price'])
                        }
                await r.set(f"user:{last_d['creator_id']}:booking", json.dumps(booking_data))

                # if history_d:
                #     booking_data_history = []
                #     for n in history_d:
                #         con = {"data": {
                #             "number": n['order_number'],
                #             "price": int(n['price']),
                #             "trip": {
                #             "attraction": {
                #                 "id": n['attr_id'],
                #                 "name": n['attr_name'],
                #                 "address": n['attr_address'],
                #                 "image": n['attr_image']
                #             },
                #             "date": n['attr_date'].strftime("%Y-%m-%d"),
                #             "time":n['attr_time']
                #             },
                #             "contact": {
                #             "name": n['contact_name'],
                #             "email": n['contact_email'],
                #             "phone": n['contact_phone']
                #             },
                #             "status": 1 if n['given_status']=='PAID' else 0
                #             }}
                #         booking_data_history.append(con)
                #     await r.set(f"user:{last_d['creator_id']}:booking_history", json.dumps(booking_data_history))

        result = await search_user_login(request,login_data.email,login_data.password)
        if isinstance(result, JSONResponse):
            return result
        access_token, last_d = result

        bt.add_task(booking_data_r, request, last_d)
        response = JSONResponse(status_code=200, content={"message": "Login successful"})
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")
        return response
                
    except (aiomysql.Error, redis.RedisError) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except ValidationError as err:
        return JSONResponse(status_code=422,content={"error": True, "message": err.errors()},headers=headers)     
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)