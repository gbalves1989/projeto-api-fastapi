from pydantic import BaseModel


class ExceptionResponseDTO(BaseModel):
    detail: str


class ExceptionRateLimitResponseDTO(BaseModel):
    error: str
    