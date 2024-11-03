from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from utils.datamodel import SignUpDataModel
from utils.token_verify_creator import token_creator
import aiomysql 
import redis.asyncio as aioredis
from datetime import timedelta

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/user") 
async def api_user_signup(request: Request, signup_data: SignUpDataModel,bt:BackgroundTasks):
    try:
        async def search_user_signup(request,sd):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute("SELECT EXISTS(SELECT 1 FROM user_info WHERE email = %s AND auth_provider IS NULL);",(sd.email,)) 
                    exists = await cursor.fetchone()  # 要注意，這邊沒辦法直接在後面加上[0]的index去呼叫，也沒辦法直接作為條件具

                    if exists[0]==0:
                        await cursor.execute("INSERT INTO `user_info` (username, password, email) VALUES (%s,%s,%s);",(sd.name,sd.password,sd.email,)) 
                        await connection.commit()
                        await cursor.execute("SELECT LAST_INSERT_ID();")
                        new_user_id = await cursor.fetchone()   # 要注意，這邊沒辦法直接在後面加上[0]的index去呼叫
                        new_user_id = new_user_id[0]
                        input_data = {"id": new_user_id,'username':sd.name,'email':sd.email, 'password':sd.password}                                        
                        print('new user join: ',input_data)

                        access_token = token_creator(data=input_data)    
                        response = JSONResponse(status_code=200, content={"ok":True})
                        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict",expires=timedelta(days=1).total_seconds())
                        return response, new_user_id

                    input_data = {"error": True,"message": "Invalid registration, duplicate email or other reasons"}
                    return JSONResponse(status_code=400,content=input_data, headers=headers), None
                
        async def booking_data_r(request, id):
            if id:
                redis_pool = request.state.async_redis_pool
                async with aioredis.Redis(connection_pool=redis_pool) as r:
                    # await r.set(f"user:{last_d['creator_id']}:booking", json.dumps(booking_data))
                    await r.set(f"user:{id}:booking_trigger_key", 'trigger_key', ex=86400)

        response, new_user_id = await search_user_signup(request,signup_data)
        bt.add_task(booking_data_r, request, new_user_id)
        return response
    
            
    except (aiomysql.Error) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except ValidationError as err:
        return JSONResponse(status_code=422,content={"error": True, "message": err.errors()},headers=headers)      
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)