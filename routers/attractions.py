from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
import mysql.connector
import json
from typing import Optional

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/attractions")
async def api_attractions(request: Request, page: int=Query(..., ge=0), keyword: Optional[str] = None):
    mydb = None
    cursor = None
    try:
        db_pool = request.state.db_pool
        connection = db_pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        # cursor = mydb_connection.cursor(dictionary=True)  # dictionary=True 這個設置就可以不必在69行使用"name":each[1]，而可以直接用
        offset_num = page*12
        keyword_format = f"%{keyword}%" 
        if keyword==None:
            cursor.execute("SELECT SQL_CALC_FOUND_ROWS * FROM processed_data LIMIT 12 OFFSET %s;", (offset_num,)) 
        else:
            cursor.execute("SELECT SQL_CALC_FOUND_ROWS * FROM processed_data WHERE mrt LIKE %s OR name LIKE %s LIMIT 12 OFFSET %s;", (keyword_format, keyword_format, offset_num,)) 
        attract_data = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS();") 
        sum_rows = cursor.fetchone()
        next_page = page+1 if sum_rows['FOUND_ROWS()'] > (page+1)*12 else None
        each_data_list = [{'id':each['id'],"name":each["name"],'category':each['category'], 'description':each['description'],'address':each['address'],'transport':each['transport'],'mrt':each['mrt'],'lat':each['lat'],'lng':each['lng'], 'images':json.loads(each['images'])} for each in attract_data]
        return JSONResponse(content={"data": each_data_list, "nextPage":next_page}, headers=headers)
        
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    finally:
        cursor.close()
        connection.close()