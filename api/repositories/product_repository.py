from prisma import Prisma

from api.dtos.requests.product_request_dto import (
    ProductCreateRequestDTO,
    ProductUpdateRequestDTO
)
from api.dtos.responses.product_response_dto import ProductResponseDTO

from typing import List


class ProductRepository:
    def __init__(self):
        self.prisma_db = Prisma()
    
    async def store_repository(
        self,
        productCreateRequestDTO: ProductCreateRequestDTO
    ) -> ProductResponseDTO:
        await self.prisma_db.connect()
        product = await self.prisma_db.product.create(
            data={
                "name": productCreateRequestDTO.name,
                "description": productCreateRequestDTO.description,
                "categoryId": productCreateRequestDTO.category_id
            }
        )
        await self.prisma_db.disconnect()

        return ProductResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            banner=product.banner
        )
        
    async def show_by_name_repository(self, name: str) -> ProductResponseDTO | None:
        await self.prisma_db.connect()
        product = await self.prisma_db.product.find_unique(
            where={"name": name}
        )
        await self.prisma_db.disconnect()

        if product != None:
            return ProductResponseDTO(
                id=product.id,
                name=product.name,
                description=product.description,
                banner=product.banner
            )

        return None
    
    async def show_repository(self, id: str) -> ProductResponseDTO | None:
        await self.prisma_db.connect()
        product = await self.prisma_db.product.find_unique(
            where={"id": id}
        )
        await self.prisma_db.disconnect()

        if product != None:
            return ProductResponseDTO(
                id=product.id,
                name=product.name,
                description=product.description,
                banner=product.banner
            )

        return None
    
    async def index_repository(self) -> List[ProductResponseDTO]:
        await self.prisma_db.connect()
        products_db = await self.prisma_db.product.find_many()
        await self.prisma_db.disconnect()
        
        return products_db

    async def index_by_category_repository(self, category_id) -> List[ProductResponseDTO]:
        await self.prisma_db.connect()
        products_db = await self.prisma_db.product.find_many(
            where={"categoryId": category_id}
        )
        await self.prisma_db.disconnect()
        
        return products_db
    
    async def update_repository(
        self,
        id: str,
        productUpdateRequestDTO: ProductUpdateRequestDTO
    ) -> ProductResponseDTO:
        await self.prisma_db.connect()
        product = await self.prisma_db.product.update(
            data={
                "name": productUpdateRequestDTO.name,
                "description": productUpdateRequestDTO.description
            },
            where={"id": id}
        )
        await self.prisma_db.disconnect()

        return ProductResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            banner=product.banner
        )
    
    async def upload_repository(self, id: str, banner: str) -> ProductResponseDTO:
        await self.prisma_db.connect()
        product = await self.prisma_db.product.update(
            data={"banner": banner},
            where={"id": id}
        )
        await self.prisma_db.disconnect()

        return ProductResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            banner=product.banner
        )
    
    async def destroy_repository(self, id: str) -> None:
        await self.prisma_db.connect()
        await self.prisma_db.product.delete({"id": id})
        await self.prisma_db.disconnect()
        