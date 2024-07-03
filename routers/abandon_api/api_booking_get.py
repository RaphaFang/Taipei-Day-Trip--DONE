from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
import mysql.connector
import time

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/booking")
async def api_booking_get(request: Request):  # ,token: str = Depends(oauth2_scheme)
    try:
        token = request.cookies.get("access_token")
        if not token:
            content_data = {"error": True, "message": "Please log-in to access the booking page."}
            return JSONResponse(status_code=403,content=content_data, headers=headers)
        
        token_output = token_verifier(token)
        if token_output:
            start_time = time.time() 
            sql_pool = request.state.sql_db_pool.get("default") 
            with sql_pool.get_connection() as connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute("""
                        SELECT * FROM user_booking_tentative
                        WHERE creator_id = %s
                        ORDER BY created_at DESC LIMIT 1;""", (token_output['id'],))
                    b = cursor.fetchone()
                    the_time = time.time() - start_time
                    print('the time cost at sql',the_time)

                    if b:
                        b['date'] = b['date'].strftime('%Y-%m-%d')
                        b['price'] = str(b['price']) 
                        content_data = {"data":{'attraction':{'id':b['attraction_id'],'name':b['name'],'address':b['address'],'image':b['image']}, "date":b['date'],"time":b['time'],"price":b['price']}}
                        return JSONResponse(content=content_data, headers=headers)
                    else:
                        content_data = {"data":None}
                        return JSONResponse(content=content_data, headers=headers)
            
    except (mysql.connector.Error) as err:
        return JSONResponse(
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    except (ValueError,Exception) as err:
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    # get 資料只能放在header，不能放在body
    # 我之前在後端用post，可以把資料型態審核交給signup_data: SignUpDataModel，api那邊就不必多寫json.loads()，現在需要多寫這個識別機制