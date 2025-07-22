from pydantic import BaseModel, EmailStr
from typing_extensions import Any


class UserInfoRequest(BaseModel):
    user_id: str
    

class UserInfoResponse(BaseModel):
    username: str


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class CreateUserResponse(BaseModel):
    id: int
    email: EmailStr