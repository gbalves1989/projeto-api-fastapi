from pydantic import BaseModel


class ProductResponseDTO(BaseModel):
    id: str
    name: str
    description: str
    banner: str
    