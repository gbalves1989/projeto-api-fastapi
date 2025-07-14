from prisma import Prisma

from api.dtos.requests.user_request_dto import (
    UserCreateRequestDTO,
    UserUpdateRequestDTO
)
from api.dtos.responses.user_response_dto import (
    UserResponseDTO,
    UserWithPassResponseDTO
)


class UserRepository:
    def __init__(self):
        self.prisma_db = Prisma()
        
    async def signup_repository(
        self,
        userCreateRequestDTO: UserCreateRequestDTO,
        hash: str
    ) -> UserResponseDTO:
        await self.prisma_db.connect()
        
        user = await self.prisma_db.user.create({
            "name": userCreateRequestDTO.name,
            "email": userCreateRequestDTO.email,
            "password": hash
        })
        
        await self.prisma_db.disconnect()

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar
        )
    
    async def show_by_email_repository(
        self, 
        email: str
    ) -> UserWithPassResponseDTO | None:
        await self.prisma_db.connect()
        user = await self.prisma_db.user.find_unique({"email": email})
        await self.prisma_db.disconnect()

        if user != None:
            return UserWithPassResponseDTO(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.password,
                avatar=user.avatar
            )

        return None
    
    async def show_repository(self, id: str) -> UserResponseDTO | None:
        await self.prisma_db.connect()
        user = await self.prisma_db.user.find_unique({"id": id})
        await self.prisma_db.disconnect()

        if user != None:
            return UserResponseDTO(
                id=user.id,
                name=user.name,
                email=user.email,
                avatar=user.avatar
            )

        return None
    
    async def update_repository(
        self,
        id: str,
        userUpdateRequestDTO: UserUpdateRequestDTO
    ) -> UserResponseDTO:
        await self.prisma_db.connect()
        user = await self.prisma_db.user.update(
            data={"name": userUpdateRequestDTO.name},
            where={"id": id}
        )
        await self.prisma_db.disconnect()

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar
        )
        
    async def update_password_repository(
        self, 
        id: str, 
        hash: str
    ) -> UserResponseDTO:
        await self.prisma_db.connect()
        user = await self.prisma_db.user.update(
            data={"password": hash},
            where={"id": id}
        )
        await self.prisma_db.disconnect()

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar
        )
    
    async def upload_repository(
        self, 
        id: str, 
        avatar: str
    ) -> UserResponseDTO:
        await self.prisma_db.connect()
        user = await self.prisma_db.user.update(
            data={"avatar": avatar},
            where={"id": id}
        )
        await self.prisma_db.disconnect()

        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            avatar=user.avatar
        )
    