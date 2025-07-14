from api.repositories.product_repository import ProductRepository
from api.exceptions.http_exception import Exception
from api.dtos.requests.product_request_dto import (
    ProductCreateRequestDTO,
    ProductUpdateRequestDTO
)
from api.dtos.responses.product_response_dto import ProductResponseDTO
from api.dtos.responses.category_response_dto import CategoryResponseDTO
from api.services.category_service import CategoryService

from fastapi import status, UploadFile

from typing import List

from utils.storage import Storage


class ProductService(ProductRepository):
    def __init__(self):
        super().__init__()
        self.exception = Exception()
        self.category_service = CategoryService()
        
    async def store_service(
        self,
        productCreateRequestDTO: ProductCreateRequestDTO
    ) -> ProductResponseDTO:
        category_exists: CategoryResponseDTO | None = await self.category_service.show_service(
            productCreateRequestDTO.category_id
        )

        if category_exists == None:
            raise self.exception.exception_error(
                "Categoria não encontrada",
                status.HTTP_404_NOT_FOUND
            )

        product_name_exists: ProductResponseDTO | None = await self.show_by_name_repository(
            productCreateRequestDTO.name
        )

        if product_name_exists != None:
            raise self.exception.exception_error(
                "Nome do produto já existe",
                status.HTTP_409_CONFLICT
            )

        product: ProductResponseDTO = await self.store_repository(productCreateRequestDTO)
        
        return product
    
    async def show_service(self, id: str) -> ProductResponseDTO:
        product: ProductResponseDTO | None = await self.show_repository(id)

        if product == None:
            raise self.exception.exception_error(
                "Categoria não encontrada",
                status.HTTP_404_NOT_FOUND
            )

        return product
    
    async def index_service(self) -> List[ProductResponseDTO]:
        products: List[ProductResponseDTO] = await self.index_repository()
        
        return products
    
    async def index_by_category_service(self, category_id: str) -> List[ProductResponseDTO]:
        products: List[ProductResponseDTO] = await self.index_by_category_repository(category_id)
        
        return products
    
    async def update_service(
        self,
        id: str,
        productUpdateRequestDTO: ProductUpdateRequestDTO
    ) -> ProductResponseDTO:
        product_exists: ProductResponseDTO | None = await self.show_repository(id)

        if (product_exists == None):
            raise self.exception.exception_error(
                "Produto não encontrado",
                status.HTTP_404_NOT_FOUND
            )

        product_name_exists: ProductResponseDTO | None = await self.show_by_name_repository(
            productUpdateRequestDTO.name
        )

        if product_name_exists != None:
            raise self.exception.exception_error(
                "Nome do produto já existe",
                status.HTTP_409_CONFLICT
            )

        product: ProductResponseDTO = await self.update_repository(
            id,
            productUpdateRequestDTO
        )

        return product
    
    async def upload_service(
        self, 
        id: str, 
        banner: UploadFile
    ) -> ProductResponseDTO:
        product: ProductResponseDTO | None = await self.show_repository(id)

        if (product == None):
            raise self.exception.exception_error(
                "Produto não encontrado",
                status.HTTP_404_NOT_FOUND
            )
        
        banner_verify: bool = Storage.verify_ext_file(banner)

        if banner_verify == False:
            raise self.exception.exception_error(
                "Tipo de arquivo inválido. Selecionar somente do tipo (.jpg, .jpeg, .png)",
                status.HTTP_406_NOT_ACCEPTABLE
            )

        banner_hash_name: str = Storage.generate_hash_filename(banner)

        if product.banner != "":
            Storage.delete_file(product.banner, "products")

        await Storage.upload_file(banner_hash_name, "products", banner)
        product: ProductResponseDTO = await self.upload_repository(id, banner_hash_name)

        return product
    
    async def destroy_service(self, id: str) -> None:
        product_exists: ProductResponseDTO | None = await self.show_repository(id)

        if (product_exists == None):
            raise self.exception.exception_error(
                "Produto não encontrado",
                status.HTTP_404_NOT_FOUND
            )
        
        if product_exists.banner != "":
            Storage.delete_file(product_exists.banner, "products")

        await self.destroy_repository(id)
        