# # from fastapi import APIRouter, Request, BackgroundTasks
# from fastapi.responses import JSONResponse
# from datetime import datetime
# from pydantic import ValidationError
# from utils.token_verify_creator import token_verifier
# from utils.datamodel import ContactAndPrimeDM
# import redis
# import json
# import aiohttp
# import aiomysql
# import os
# import redis
# import redis.asyncio as aioredis 

# router = APIRouter()
# headers = {"Content-Type": "application/json; charset=utf-8"}

# @router.get("/api/orders/history")
# async def prime_order(request: Request, cp:ContactAndPrimeDM, bt:BackgroundTasks):  # 這邊多試試看BackgroundTasks
#     # try:
#         token = request.cookies.get("access_token")
#         if not token:
#             content_data = {"error": True, "message": "You did not got the token in cookies, how to you even came to the order step???"}
#             return JSONResponse(status_code=403,content=content_data, headers=headers)
#         token_output = token_verifier(token)

#         async def search_user_login(request,e,p):
#             sql_pool = request.state.async_sql_pool 
#             async with sql_pool.acquire() as connection:
#                 async with connection.cursor(aiomysql.DictCursor) as cursor:
#                     await cursor.execute("SELECT * FROM user_info WHERE email = %s AND password = %s;", (e,p,)) 
#                     data =  await cursor.fetchone()
#                     if data:
#                         input_data = {"id": data['id'],'username':data['username'],'email':data['email'], 'password':data['password']}                                        
#                         access_token = token_creator(data=input_data)

#                         await cursor.execute("SELECT * FROM user_booking_tentative WHERE creator_id = %s;", (data['id'],)) 
#                         last_d = await cursor.fetchone()

#                         await cursor.execute("SELECT * FROM user_booking_finalized WHERE creator_id = %s AND given_status = 'PAID' ORDER BY created_at LIMIT 10;", (data['id'],))
#                         history_d = await cursor.fetchall()
        