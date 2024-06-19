import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import  HTTPException


ALGORITHM = "RS256"
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')

def token_creator(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(days=7)})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def token_verifier(token: str):
    try:
        decoded_jwt = jwt.decode(token, PUBLIC_KEY, algorithms=ALGORITHM)
        return decoded_jwt
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="the JWT token could not be validated",
            headers={"WWW-Authenticate": "Bearer"},
        )