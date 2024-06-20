import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import  HTTPException


ALGORITHM = "RS256"
private_key_path = os.getenv("PRIVATE_KEY_PATH")
with open(private_key_path, 'r') as file:
    PRIVATE_KEY = file.read()
public_key_path = os.getenv("PUBLIC_KEY_PATH")
with open(public_key_path, 'r') as file:
    PUBLIC_KEY = file.read()

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