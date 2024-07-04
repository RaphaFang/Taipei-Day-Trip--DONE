from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
from pydantic import ValidationError
from utils.datamodel import BookingDataMode
import json
import redis
import redis.asyncio as aioredis 

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/booking")   #! changed to -> booking
async def api_booking_post_redis(request: Request, j_data:BookingDataMode, bt:BackgroundTasks): # , token: str = Depends(oauth2_scheme)  # 這裡還有範一個錯 寫成j_data＝BookingDataMode
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "Please log-in to access the booking page."}
            return JSONResponse(status_code=403,content=content_data, headers=headers)
        input_token = token_verifier(token)

        if input_token:
            async def post_user_r(request, id, j):
                redis_pool = request.state.async_redis_pool
                async with aioredis.Redis(connection_pool=redis_pool) as r:
                    booking_data = {
                        "attraction_id": j.attractionId,
                        "name": j.name,
                        "address": j.address,
                        "image": j.image,
                        "date": j.date,
                        "time": j.time,
                        "price": j.price
                    }
                    await r.set(f"user:{id}:booking", json.dumps(booking_data))
            # await post_user_r(request,input_token['id'], j_data)
            bt.add_task(post_user_r, request, input_token['id'], j_data)
# 
            content_data={"ok": True}
            return JSONResponse(status_code=200,content=content_data, headers=headers)

    except redis.RedisError as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except ValidationError as err:
        return JSONResponse(status_code=422,content={"error": True, "message": err.errors()},headers=headers)   
    except (ValueError,Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)
    
    # 如果資料放在 header ，ValidationError 的驗證會搶在所有api運作邏輯之前執行，解決方式是把資料放在body，不放在header
    # 原先放在header，還是要注意 data 要在 token 前面，因為 token有默認值，前者沒有...