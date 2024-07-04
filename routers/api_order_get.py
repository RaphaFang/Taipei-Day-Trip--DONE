from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import mysql.connector
import aiomysql

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/order/{orderNum}")
async def prime_order_get(request: Request, orderNum:int): 
    try:
        # 提供用戶直接搜尋的功能，所以不一定要登入token，檢查關閉
        # 20240703154535418177
        async def search_num(orderNum):
                sql_pool = request.state.async_sql_db_pool 
                async with sql_pool.acquire() as connection:
                    async with connection.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute("""SELECT * FROM user_booking_finalized WHERE order_number= %s """,(orderNum))
                        return await cursor.fetchone()
        result = await search_num(orderNum)
        if result:
            con = {"data": {
                        "number": result['order_number'],
                        "price": int(result['price']),
                        "trip": {
                        "attraction": {
                            "id": result['attr_id'],
                            "name": result['attr_name'],
                            "address": result['attr_address'],
                            "image": result['attr_image']
                        },
                        "date": result['attr_date'].strftime("%Y-%m-%d"),
                        "time":result['attr_time']
                        },
                        "contact": {
                        "name": result['contact_name'],
                        "email": result['contact_email'],
                        "phone": result['contact_phone']
                        },
                        "status": 1 if result['given_status']=='PAID' else 0
                    }}
            return JSONResponse(status_code=200,content=con,headers=headers)
        else:
            con = { "error": True, "message": 'You might enter an invalid order-number, please check again.'}
            return JSONResponse(status_code=400,content=con,headers=headers)

    except (mysql.connector.Error) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except KeyError as err:
        return JSONResponse(status_code=400, content={"error": True, "message": f"Missing key: {str(err)}"}, headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
   