from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
import redis
import json

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/booking")  #! changed to -> booking
async def api_booking_get(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "Please log-in to access the booking page."}
            return JSONResponse(status_code=403,content=content_data, headers=headers)
        
        token_output = token_verifier(token)
        if token_output:
            redis_pool = request.state.redis_db_pool.get("default") 
            r = redis.Redis(connection_pool=redis_pool)
            b = r.get(f"user:{token_output['id']}:booking")

            if b:
                b = json.loads(b)
                print('-----')
                print(b)                
                print('-----')
                content_data = {"data":{'attraction':{'id':b['attraction_id'],'name':b['name'],'address':b['address'],'image':b['image']}, "date":b['date'],"time":b['time'],"price":b['price']}}
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