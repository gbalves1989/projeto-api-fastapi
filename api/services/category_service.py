from api.repositories.category_repository import CategoryRepository
from api.repositories.product_repository import ProductRepository
from api.dtos.requests.category_request_dto import (
    CategoryCreateRequestDTO,
    CategoryUpdateRequestDTO
)
from api.dtos.responses.product_response_dto import ProductResponseDTO
from api.dtos.responses.category_response_dto import CategoryResponseDTO
from api.exceptions.http_exception import Exception

from fastapi import status

from typing import List


class CategoryService(CategoryRepository):
    def __init__(self):
        super().__init__()
        self.exception = Exception()
        self.product_repository = ProductRepository
    
    async def store_service(
        self, 
        user_id: str,
        categoryCreateRequestDTO: CategoryCreateRequestDTO) -> CategoryResponseDTO:
        category_name_exists: CategoryResponseDTO | None = await self.show_by_name_repository(
            categoryCreateRequestDTO.name
        )

        if category_name_exists != None:
            raise self.exception.exception_error(
                "Categoria já está cadastrada",
                status.HTTP_409_CONFLICT
            )

        category: CategoryResponseDTO = await self.store_repository(user_id, categoryCreateRequestDTO)
        
        return category
    
    async def show_service(self, id: str) -> CategoryResponseDTO | None:
        category: CategoryResponseDTO | None = await self.show_repository(id)

        if category == None:
            raise self.exception.exception_error(
                "Categoria não encontrada",
                status.HTTP_404_NOT_FOUND
            )

        return category
    
    async def index_service(self, user_id: str) -> List[CategoryResponseDTO]:
        categories: List[CategoryResponseDTO] = await self.index_repository(user_id)
        
        return categories
    
    async def update_service(
        self,
        id: str,
        categoryUpdateRequestDTO: CategoryUpdateRequestDTO
    ) -> CategoryResponseDTO:
        category_exists: CategoryResponseDTO | None = await self.show_repository(id)

        if category_exists == None:
            raise self.exception.exception_error(
                "Categoria não encontrada",
                status.HTTP_404_NOT_FOUND
            )

        category_name_exists: CategoryResponseDTO | None = await self.show_by_name_repository(
            categoryUpdateRequestDTO.name
        )

        if category_name_exists != None:
            raise self.exception.exception_error(
                "Nome da categoria já existe",
                status.HTTP_409_CONFLICT
            )

        category: CategoryResponseDTO = await self.update_repository(
            id,
            categoryUpdateRequestDTO
        )

        return category
    
    async def destroy_service(self, id: str) -> None:
        category: CategoryResponseDTO | None = await self.show_repository(id)

        if category == None:
            raise self.exception.exception_error(
                "Categoria não encontrada",
                status.HTTP_404_NOT_FOUND
            )

        products: List[ProductResponseDTO] = await self.product_repository.index_by_category_repository(id)
        
        if products != []:
            raise self.exception.exception_error(
                "Categoria possui produtos cadastrados",
                status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        await self.destroy_repository(id)
        