from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import json
from typing import Optional
app=FastAPI()

import mysql.connector
import os
sql_password = os.getenv('SQL_PASSWORD')
sql_username = os.getenv('SQL_USER')
db_config = {
    'host': '52.4.229.207',
    'user': sql_username,
    'password': sql_password,
    'database': 'basic_db',
    'port':3306
}
headers = {"Content-Type": "application/json; charset=utf-8"}

@app.get("/api/attractions")
def api_attractions(page: int=Query(..., ge=0), keyword: Optional[str] = None):
    print(f"page = {page}, keyword = {keyword}")
    try:
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor()
        offset_num = page*12
        keyword_format = f"%{keyword}%"  # 這邊不四多加上"""

        if keyword==None:
            cursor.execute("SELECT SQL_CALC_FOUND_ROWS * FROM processed_data LIMIT 12 OFFSET %s;", (offset_num,)) 
        else:
            cursor.execute("SELECT SQL_CALC_FOUND_ROWS * FROM processed_data WHERE mrt LIKE %s OR name LIKE %s LIMIT 12 OFFSET %s;", (keyword_format, keyword_format, offset_num,)) 
        attract_data = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS();") 
        sum_rows = cursor.fetchone()[0] 

        next_page = page+1 if sum_rows > (page+1)*12 else None
        each_data_list = [{'id':each[0],"name":each[1],'category':each[2], 'description':each[3],'address':each[4],'transport':each[5],'mrt':each[6],'lat':each[7],'lng':each[8], 'images':json.loads(each[9])} for each in attract_data]
        return JSONResponse(content={"data": each_data_list, "nextPage":next_page}, headers=headers)
        
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    finally:
        cursor.close()
        mydb.close()

@app.get("/api/attraction/{id}")  
def api_attractions(id=int): # page:int, keyword:str, 
    # print(id)
    try:
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM processed_data WHERE id = %s", (id,)) 
        attract_data = cursor.fetchone()
        print(attract_data)

        if attract_data:
            return JSONResponse(content={"data":{'id':attract_data[0],"name":attract_data[1],'category':attract_data[2], 'description':attract_data[3],'address':attract_data[4],'transport':attract_data[5],'mrt':attract_data[6],'lat':attract_data[7],'lng':attract_data[8], 'images':json.loads(attract_data[9])}},
                        headers=headers)
        else:
            return JSONResponse(    
                status_code=400,
                content={"error": True, "message": "inserted id out of range, valid id start from 1 to 58"},
                headers=headers
            )
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    finally:
        cursor.close()
        mydb.close()


@app.get("/api/mrts")
def api_mrts():
    mydb = None
    cursor = None
    try:
        # raise mysql.connector.Error("Manually triggered error for testing")
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor()
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
            mydb.close()

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")