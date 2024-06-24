from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import mysql.connector
import time

# import aiomysql


router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/mrts")
async def api_mrts(request: Request):
    try:
        start_time = time.time()
        db_pool = request.state.db_pool.get("basic_db") 
        with db_pool.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT mrt, COUNT(DISTINCT name) as count FROM processed_data WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY count DESC;") 
                mrts_counted = cursor.fetchall()
                content_data = {"data":[n[0] for n in mrts_counted]}
                set_time = time.time() - start_time
                print(set_time)
                return JSONResponse(content=content_data, headers=headers)
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
# start_time = time.time()
# found_in_list = search_word in words
# set_time = time.time() - start_time