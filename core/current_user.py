from fastapi import Depends, status

from api.dtos.responses.user_response_dto import UserResponseDTO
from api.exceptions.http_exception import Exception
from api.repositories.user_repository import UserRepository

from jose import jwt, JWTError

from core.config import settings

from utils.auth_schema import oauth2_schema


class CurrentUser:
    def __init__(self) -> None:
        self.exception = Exception()
        self.user_repository = UserRepository()
    
    async def get_current_user(
        self,
        token: str = Depends(oauth2_schema)
    ) -> UserResponseDTO:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.ALGORITHM],
                options={"verify_aud": False}
            )

            username: str = payload.get("sub")

            if username is None:
                raise exception.exception_error_credential(
                    message="Token inválido ou expirado",
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user: UserResponseDTO | None = await self.user_repository.show_repository(
                username
            )

            if user == None:
                raise self.exception.exception_error_credential(
                    message="Token inválido ou expirado",
                    status=status.HTTP_401_UNAUTHORIZED
                )

            return user
        
        except JWTError:
            raise self.exception.exception_error_credential(
                message="Token inválido ou expirado",
                status=status.HTTP_401_UNAUTHORIZED
            )
            