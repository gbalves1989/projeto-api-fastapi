from pydantic import BaseModel, EmailStr

from typing import List


class UserResponseDTO(BaseModel):
    id: str
    name: str
    email: EmailStr
    avatar: str
    

class UserWithPassResponseDTO(UserResponseDTO):
    password: str


class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str
    