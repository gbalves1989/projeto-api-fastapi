from prisma import Prisma

from api.dtos.requests.category_request_dto import (
    CategoryCreateRequestDTO,
    CategoryUpdateRequestDTO
)
from api.dtos.responses.category_response_dto import CategoryResponseDTO

from typing import List


class CategoryRepository:
    def __init__(self):
        self.prisma_db = Prisma()
    
    async def store_repository(
        self, 
        user_id: str,
        categoryCreateRequestDTO: CategoryCreateRequestDTO
    ) -> CategoryResponseDTO:
        await self.prisma_db.connect()
        category = await self.prisma_db.category.create({
            "name": categoryCreateRequestDTO.name,
            "userId": user_id
        })
        await self.prisma_db.disconnect()
        
        return CategoryResponseDTO(
            id=category.id,
            name=category.name
        )
        
    async def show_by_name_repository(
        self, 
        name: str
    ) -> CategoryResponseDTO | None:
        await self.prisma_db.connect()
        category = await self.prisma_db.category.find_unique({"name": name})
        await self.prisma_db.disconnect()

        if category != None:
            return CategoryResponseDTO(
                id=category.id,
                name=category.name
            )

        return None

    async def show_repository(
        self, 
        id: str
    ) -> CategoryResponseDTO | None:
        await self.prisma_db.connect()
        category = await self.prisma_db.category.find_unique({"id": id})
        await self.prisma_db.disconnect()

        if category != None:
            return CategoryResponseDTO(
                id=category.id,
                name=category.name
            )

        return None

    async def index_repository(self, user_id: str) -> List[CategoryResponseDTO]:
        await self.prisma_db.connect()
        categories = await self.prisma_db.category.find_many(where={"userId": user_id})
        await self.prisma_db.disconnect()

        return categories
    
    async def update_repository(
        self,
        id: str,
        categoryUpdateRequestDTO: CategoryUpdateRequestDTO
    ) -> CategoryResponseDTO:
        await self.prisma_db.connect()
        category = await self.prisma_db.category.update(
            data={"name": categoryUpdateRequestDTO.name},
            where={"id": id}
        )
        await self.prisma_db.disconnect()

        return CategoryResponseDTO(
            id=category.id,
            name=category.name
        )

    async def destroy_repository(self, id: str) -> None:
        await self.prisma_db.connect()
        await self.prisma_db.category.delete({"id": id})
        await self.prisma_db.disconnect()
        