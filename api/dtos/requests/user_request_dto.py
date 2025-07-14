from pydantic import BaseModel, EmailStr


class UserCreateRequestDTO(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    
class UserUpdateRequestDTO(BaseModel):
    name: str   


class UserUpdatePassRequestDTO(BaseModel):
    password: str 


class UserLoginRequestDTO(BaseModel):
    email: str
    password: str
    