from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from utils.token_verify_creator import token_verifier
from fastapi.security import OAuth2PasswordBearer