from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
import mysql.connector

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

from pydantic import BaseModel, Field, validator
import re

# class DataModel(BaseModel):
#     signup_name: str
#     signup_email: str
#     signup_password: str
#     @validator('signup_name')
#     def validate_email(cls, v):
#         if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", v):
#             raise ValueError('signup_name did not match the require')
#         return v
#     @validator('signup_email')
#     def validate_password(cls, v):
#         if not re.match(r"^[A-Za-z0-9@#$%]{4,8}$", v):
#             raise ValueError('signup_email did not match the require')
#         return v
#     @validator('signup_password')
#     def validate_tel(cls, v):
#         if not re.match(r"^[0-9]{4}-[0-9]{3}-[0-9]{3}$", v):
#             raise ValueError('signup_password did not match the require')
#         return v

@router.get("/api/user")
async def api_user(request: Request,signup_name: str = Form(...), signup_email: str = Form(...), signup_password: str= Form(...)):
    try:
        db_pool = request.state.db_pool.get("basic_db") 
        with db_pool.get_connection() as connection:
            with connection.cursor() as cursor:
                
                cursor.execute("SELECT mrt, COUNT(DISTINCT name) as count FROM processed_data WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY count DESC;") 
                
                mrts_counted = cursor.fetchall()
                con_d = {"data":[n[0] for n in mrts_counted]}


            return JSONResponse(content=con_d, headers=headers)
    
    except mysql.connector.Error as err:
        return JSONResponse(    
            status_code=500,
            content={"error": True, "message": str(err)},
            headers=headers
        )
    except ValueError as e:
        return JSONResponse(    
            status_code=400,
            content={"error": True, "message": str(err)},
            headers=headers
        )
