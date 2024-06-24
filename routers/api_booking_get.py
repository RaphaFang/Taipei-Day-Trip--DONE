# from fastapi import APIRouter, Request, Depends, HTTPException
# from fastapi.responses import JSONResponse
# import mysql.connector
# from utils.token_verify_creator import token_verifier
# from fastapi.security import OAuth2PasswordBearer
# import aiomysql


# router = APIRouter()
# headers = {"Content-Type": "application/json; charset=utf-8"}

# @router.get("/api/booking")
# async def api_user_get(request: Request,token: str = Depends(oauth2_scheme)):
