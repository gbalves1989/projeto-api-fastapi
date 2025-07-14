from fastapi import HTTPException


class Exception:
    def __init__(self, headers={"WWW-Authenticate": "Bearer"}) -> None:
        self.headers = headers
    
    def exception_error(self, message: str, status: int) -> HTTPException:
        return HTTPException(
            detail=message,
            status_code=status
        )
    
    def exception_error_credential(self, message: str, status: int) -> HTTPException:
        return HTTPException(
            detail=message,
            status_code=status,
            headers=self.headers
        )
        