from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from datetime import datetime
import mysql.connector
from pydantic import ValidationError
from utils.token_verify_creator import token_verifier
from utils.datamodel import ContactAndPrimeDM
import redis
import json
import aiohttp
import aiomysql
import os
import redis
import redis.asyncio as aioredis 

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/orders")
async def prime_order(request: Request, cp:ContactAndPrimeDM, bt:BackgroundTasks):  # 這邊多試試看BackgroundTasks
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "You did not got the token in cookies, how to you even came to the order step???"}
            return JSONResponse(status_code=403,content=content_data, headers=headers)
        token_output = token_verifier(token)

        if token_output:

            async def sending_prime(cp):
                payload={"prime": cp.prime, "partner_key": os.getenv('TAP_PARTNER_KEY'), "merchant_id": os.getenv("MERCHANT_ID"), "details":"TapPay Test", "amount": cp.price, "cardholder": { "phone_number": cp.phone, "name": cp.name, "email": cp.email }, "remember": True}
                hd = {"Content-Type": "application/json","x-api-key": os.getenv('TAP_PARTNER_KEY')}
                url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=hd) as response:
                        return await response.json()

            async def post_user_redis(request, id, r_status):
                redis_pool = request.state.async_redis_pool
                async with aioredis.Redis(connection_pool=redis_pool) as r:
                    data = await r.get(f"user:{id}:booking")
                    if r_status:
                        await r.delete(f"user:{id}:booking")
                    if data:
                        data = json.loads(data)
                    return  data
                
            async def put_info_in_db(request, result, redis_data, cp, SoF, id, generate_order_id):
                sql_pool = request.state.async_sql_pool 
                async with sql_pool.acquire() as connection:
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute("""
                                INSERT INTO user_booking_finalized (
                                    order_number,creator_id,given_status,bank_status,bank_msg,
                                             price,attr_id,attr_name,attr_address,attr_image,attr_date,attr_time,
                                             contact_name,contact_email,contact_phone,
                                             card_secret,card_info
                                )SELECT %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s;
                            """, (generate_order_id,id,SoF,result['status'],result['msg'],
                                   redis_data['price'],redis_data['attraction_id'], redis_data['name'], redis_data['address'], redis_data['image'], redis_data['date'], redis_data['time'],
                                      cp.name, cp.email,cp.phone,
                                      json.dumps(result.get('card_secret')),json.dumps(result.get('card_info'))))
                        await connection.commit()


            result = await sending_prime(cp)
            generate_order_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
            if result.get('status') == 0:
                redis_data = await post_user_redis(request,token_output['id'],True)
                SoF = 'PAID'
                sc=200
                con = {"data": {"number": generate_order_id,"payment": {"status": 0,"message": "successfully paid"}}}

            else:
                redis_data = await post_user_redis(request,token_output['id'],False)
                SoF = 'UNPAID'
                sc= 400
                con = {'error':True, "message":result.get('msg')}
            bt.add_task(put_info_in_db, request, result, redis_data, cp, SoF, token_output['id'], generate_order_id)
            return JSONResponse(status_code=sc, content=con, headers=headers)

    except (mysql.connector.Error, redis.RedisError) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except ValidationError as err:
        return JSONResponse(status_code=422,content={"error": True, "message": "Invalid user-info formate detected, please make sure the correct formate."},headers=headers)      
    except KeyError as err:
        return JSONResponse(status_code=400, content={"error": True, "message": f"Missing key: {str(err)}"}, headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
   


            # 如果要提供用戶「未登入」查詢，那麼存到redis就不必做了，因為沒有token，沒token就沒有id
               # prime_return_data = {"data": {
            #                 "number": generate_order_id,
            #                 "price": b['price'],
            #                 "trip": {
            #                 "attraction": {"id": b['attraction_id'],"name": b['name'],"address":b['address'],"image":b['image']                            },
            #                 "date":b['date'],
            #                 "time":b['time']
            #                 },
            #                 "contact": {"name": cp.name,"email": cp.email,"phone": cp.phone},
            #                 "status": result.get('status')}}
    

                    # r.set(f"user:{token_output['id']}:booking_result", json.dumps(prime_return_data))

