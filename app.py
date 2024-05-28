from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
app=FastAPI()

import mysql.connector
import os
sql_password = os.getenv('SQL_PASSWORD')
sql_username = os.getenv('SQL_USER')
db_config = {
    'host': 'localhost',
    'user': sql_username,
    'password': sql_password,
    'database': 'basic_db',
}


@app.get("/api/mrts")
def api_mrts():
    try:
        # raise mysql.connector.Error("Manually triggered error for testing")
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor()
        cursor.execute("SELECT mrt, COUNT(*) as count FROM processed_data GROUP BY mrt ORDER BY count DESC;") 
        mrts_counted = cursor.fetchall()
        return [n[0] for n in mrts_counted]
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)}
        )
    finally:
        cursor.close()
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