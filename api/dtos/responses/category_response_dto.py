from pydantic import BaseModel


class CategoryResponseDTO(BaseModel):
    id: str
    name: str
