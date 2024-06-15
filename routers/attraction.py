from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
import mysql.connector


import json
from typing import Optional

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}


@router.get("/api/attraction/{id}")  
async def api_attractions(request: Request, id=int): 
    try:
        db_pool = request.state.db_pool.get("basic_db")
        connection = db_pool.get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM processed_data WHERE id = %s", (id,)) 
        attract_data = cursor.fetchone()
        if attract_data:
            attract_data['images'] = json.loads(attract_data['images'])
            return JSONResponse(content={"data": attract_data},
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
        connection.close()