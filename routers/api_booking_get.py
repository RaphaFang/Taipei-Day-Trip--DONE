from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
import json
import redis
import redis.asyncio as aioredis 

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/booking")  #! changed to -> booking
async def api_booking_get(request: Request):
    try:
        token = request.cookies.get("access_token")
        token_response = token_verifier(token)
        if isinstance(token_response, JSONResponse):
            return token_response
        token_output = token_response

        if token_output:
            async def get_user_r(request, id):
                redis_pool = request.state.async_redis_pool
                async with aioredis.Redis(connection_pool=redis_pool) as r:
                    return  await r.get(f"user:{id}:booking")
            redis_data = await get_user_r(request,token_output['id'])

            if redis_data:
                redis_data = json.loads(redis_data)
                content_data = {"data":{'attraction':{'id':redis_data['attraction_id'],'name':redis_data['name'],'address':redis_data['address'],'image':redis_data['image']}, "date":redis_data['date'],"time":redis_data['time'],"price":redis_data['price']}}
                return JSONResponse(content=content_data, headers=headers)
            else:
                content_data = {"data":None}
                return JSONResponse(content=content_data, headers=headers)
            
    except redis.RedisError as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (ValueError,Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)
    
    # get 資料只能放在header，不能放在body
    # 我之前在後端用post，可以把資料型態審核交給signup_data: SignUpDataModel，api那邊就不必多寫json.loads()，現在需要多寫這個識別機制

            # redis_pool = request.state.redis_db_pool.get("default") 
            # r = redis.Redis(connection_pool=redis_pool)
            # b = r.get(f"user:{token_output['id']}:booking")