from pydantic import BaseModel


class CategoryCreateRequestDTO(BaseModel):
    name: str
    
    
class CategoryUpdateRequestDTO(BaseModel):
    name: str 
    