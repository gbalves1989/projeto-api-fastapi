from pydantic import BaseModel


class ProductCreateRequestDTO(BaseModel):
    name: str
    description: str
    category_id: str
    
    
class ProductUpdateRequestDTO(BaseModel):
    name: str 
    description: str
    