from pydantic import BaseModel, Field, validator
import re

class SignUpDataModel(BaseModel):
    name: str
    email: str
    password: str
    @validator('name')
    def validate_signup_name(cls, v):
        print(v)
        # if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", v):
        #     raise ValueError('signup_name did not match the require')
        return v
    @validator('email')
    def validate_signup_email(cls, v):
        print(v)

        # if not re.match(r"^[A-Za-z0-9@#$%]{4,8}$", v):
        #     raise ValueError('signup_email did not match the require')
        return v
    @validator('password')
    def validate_signup_password(cls, v):
        print(v)

        # if not re.match(r"^[0-9]{4}-[0-9]{3}-[0-9]{3}$", v):
        #     raise ValueError('signup_password did not match the require')
        return v
class SignInDataModel(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_signin_email(cls, v):
        return v

    @validator('password')
    def validate__signin_password(cls, v):
        return v