from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import mysql.connector

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/mrts")
async def api_mrts(request: Request):
    mydb = None
    cursor = None
    try:
        db_pool = request.state.db_pool
        connection = db_pool.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT mrt, COUNT(DISTINCT name) as count FROM processed_data WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY count DESC;") 
        mrts_counted = cursor.fetchall()
        return JSONResponse(content={"data":[n[0] for n in mrts_counted]}, headers=headers)
    
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    finally:
        if cursor:
            cursor.close()
        if mydb:
            connection.close()

# ----------------------------------
# from fastapi import APIRouter, Request
# from fastapi.responses import JSONResponse

# router = APIRouter()

# @router.get("/api/mrts")
# async def get_mrt(request: Request):
#     try:
#         db_pool = request.state.db_pool.get("spot")
#         with db_pool.get_connection() as con:
#             with con.cursor() as cursor:
#                 cursor.execute("SELECT MRT, COUNT(MRT) AS count FROM spots GROUP BY MRT ORDER BY count DESC")
#                 results = cursor.fetchall()
#             mrt_data = [result[0] for result in results]
#             data = {"data": mrt_data}
#             return JSONResponse(content=data, media_type="application/json")
#     except Exception as e:
#         print(f"Unhandled exception: {e}")
#         data = {"error": True, "message": "伺服器內部錯誤"}
#         return JSONResponse(status_code=500, content=data, media_type="application/json")