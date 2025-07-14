from api.repositories.user_repository import UserRepository
from api.dtos.responses.user_response_dto import (
    UserResponseDTO,
    UserWithPassResponseDTO
)
from api.dtos.requests.user_request_dto import (
    UserCreateRequestDTO,
    UserLoginRequestDTO,
    UserUpdateRequestDTO,
    UserUpdatePassRequestDTO
)
from api.exceptions.http_exception import Exception

from fastapi import status, UploadFile

from utils.storage import Storage
from utils.hash import Hash


class UserService(UserRepository):
    def __init__(self):
        super().__init__()
        self.exception = Exception()
        self.hash = Hash()
    
    async def signup_service(
        self, 
        userCreateRequestDTO: UserCreateRequestDTO
    ) -> UserResponseDTO:
        email_exists: UserResponseDTO | None = await self.show_by_email_repository(
            userCreateRequestDTO.email
        )

        if email_exists != None:
            raise self.exception.exception_error(
                "E-mail já está cadastrado",
                status.HTTP_409_CONFLICT
            )

        hash_password: str = self.hash.generate_hash_password(
            userCreateRequestDTO.password
        )

        user: UserResponseDTO = await self.signup_repository(
            userCreateRequestDTO,
            hash_password
        )

        return user
    
    async def signin_service(
        self,
        userLoginRequestDTO: UserLoginRequestDTO
    ) -> UserResponseDTO:
        user: UserWithPassResponseDTO | None = await self.show_by_email_repository(
            userLoginRequestDTO.email
        )

        if user == None:
            raise self.exception.exception_error(
                "Credenciais inválidas",
                status.HTTP_400_BAD_REQUEST
            )

        if not self.hash.verify_password(
            userLoginRequestDTO.password, 
            user.password
        ):
            raise self.exception.exception_error(
                "Credenciais inválidas",
                status.HTTP_400_BAD_REQUEST
            )

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar
        )
    
    async def update_service(
        self,
        id: str,
        userUpdateRequestDTO: UserUpdateRequestDTO
    ) -> UserResponseDTO:
        user_exists: UserResponseDTO | None = await self.show_repository(id)
        
        if user_exists == None:
            raise self.exception.exception_error(
                "Usuário não encontrado",
                status.HTTP_404_NOT_FOUND
            )
        
        user: UserResponseDTO = await self.update_repository(
            id, 
            userUpdateRequestDTO
        )
        
        return user
    
    async def update_password_service(
        self,
        id: str,
        userUpdatePassRequestDTO: UserUpdatePassRequestDTO
    ) -> UserResponseDTO:
        user_exists: UserResponseDTO | None = await self.show_repository(id)
        
        if user_exists == None:
            raise self.exception.exception_error(
                "Usuário não encontrado",
                status.HTTP_404_NOT_FOUND
            )
        
        hash: str = self.hash.generate_hash_password(userUpdatePassRequestDTO.password)

        user: UserResponseDTO = await self.update_password_repository(id, hash)
        
        return user

    async def upload_service(
        self,
        user_logged: UserResponseDTO, 
        avatar: UploadFile
    ) -> UserResponseDTO:
        avatar_verify: bool = Storage.verify_ext_file(avatar)

        if avatar_verify == False:
            raise self.exception.exception_error(
                "Tipo de arquivo inválido. Selecione somente arquivos do tipo (.jpg, .jpeg, .png)",
                status.HTTP_406_NOT_ACCEPTABLE
            )

        avatar_hash_name: str = Storage.generate_hash_filename(avatar)

        if user_logged.avatar != "":
            Storage.delete_file(user_logged.avatar, "users")

        await Storage.upload_file(avatar_hash_name, "users", avatar)
        user: UserResponseDTO = await self.upload_repository(
            user_logged.id, 
            avatar_hash_name
        )

        return user
    