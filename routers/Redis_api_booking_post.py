from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
from pydantic import ValidationError
from utils.datamodel import BookingDataMode
import redis
import json

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/booking")   #! changed to -> booking
async def api_booking_post_redis(request: Request, j_data:BookingDataMode): # , token: str = Depends(oauth2_scheme)  # 這裡還有範一個錯 寫成j_data＝BookingDataMode
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "Please log-in to access the booking page."}
            return JSONResponse(status_code=403,content=content_data, headers=headers)
        
        print('2. the data from booking_redis :: ',j_data)
        input_token = token_verifier(token)
        if input_token:
            
            redis_pool = request.state.redis_db_pool.get("default") 
            r = redis.Redis(connection_pool=redis_pool)
            booking_data = {
                "attraction_id": j_data.attractionId,
                "name": j_data.name,
                "address": j_data.address,
                "image": j_data.image,
                "date": j_data.date,
                "time": j_data.time,
                "price": j_data.price
            }
            r.set(f"user:{input_token['id']}:booking", json.dumps(booking_data))
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