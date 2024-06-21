from pydantic import BaseModel, Field, validator, EmailStr 
import re

class SignUpDataModel(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('name')
    def validate_signup_name(cls, v):
        # if len(v) < 8 or not re.match(r'^[A-Za-z0-9!@#$%^&*]+$', v):
        #     raise ValueError('The name must be at least 8 characters long, blank space is not allowed.')
        return v
    
    @validator('password')
    def validate_signup_password(cls, v):
        # if len(v) < 8:
        #     raise ValueError('The password must be exactly 8 characters long, blank space is not allowed.')
        # if not re.search(r'[A-Z]', v):
        #     raise ValueError('The password must include at least one uppercase letter.')
        # if not re.search(r'[0-9]', v):
        #     raise ValueError('The password must include at least one number.')
        # if not re.search(r'[!@#$%^&*]', v):
        #     raise ValueError('The password must include at least one special character (!@#$%^&*).')
        return v
    
class SignInDataModel(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def validate__signin_password(cls, v):
        # if len(v) < 8:
        #     raise ValueError('The password must be at least 8 characters long.')
        return v