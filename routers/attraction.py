from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
import mysql.connector
from db import mydb_pool

import json
from typing import Optional

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}


@router.get("/api/attraction/{id}")  
def api_attractions(id=int): 
    try:
        mydb_connection = mydb_pool.get_connection() 
        cursor = mydb_connection.cursor(dictionary=True) 
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
        mydb_connection.close()