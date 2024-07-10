from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
import redis
import aiomysql 

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/orders/history")
async def prime_order(request: Request):  # 這邊多試試看BackgroundTasks
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "You did not got the token in cookies, how to you even came to this step???"}
            return JSONResponse(status_code=403,content=content_data, headers=headers)
        token_output = token_verifier(token)

        async def search_user_booking_history(request,id):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("SELECT * FROM user_booking_finalized WHERE creator_id = %s AND given_status = 'PAID' ORDER BY created_at LIMIT 10;", (id,)) 
                    return await cursor.fetchall()
        content_data = await search_user_booking_history(request,token_output['id'])

        if content_data:
            booking_data_history = []
            for n in content_data:
                con = {"data": {
                        "number": n['order_number'],
                        "price": int(n['price']),
                        "trip": {
                        "attraction": {
                            "id": n['attr_id'],
                            "name": n['attr_name'],
                            "address": n['attr_address'],
                            "image": n['attr_image']
                        },
                        "date": n['attr_date'].strftime("%Y-%m-%d"),
                        "time":n['attr_time']
                        },
                        "contact": {
                        "name": n['contact_name'],
                        "email": n['contact_email'],
                        "phone": n['contact_phone']
                        },
                        "status": 1 if n['given_status']=='PAID' else 0
                        }}
                booking_data_history.append(con)

            return JSONResponse(content=booking_data_history, headers=headers)
        else:
             content_data =  {"data":None}
             return JSONResponse(content=content_data, headers=headers)

    except (aiomysql.Error, redis.RedisError) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)
        