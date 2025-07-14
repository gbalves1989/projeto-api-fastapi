from fastapi import APIRouter, status, UploadFile, Depends, Request
from fastapi_pagination import Page, paginate
from fastapi.responses import FileResponse

from api.dtos.requests.product_request_dto import (
    ProductCreateRequestDTO,
    ProductUpdateRequestDTO
)
from api.dtos.responses.product_response_dto import ProductResponseDTO
from api.dtos.responses.exception_response_dto import (
    ExceptionResponseDTO,
    ExceptionRateLimitResponseDTO
)
from api.services.product_service import ProductService
from api.dtos.responses.user_response_dto import UserResponseDTO

from typing import List

from slowapi import Limiter
from slowapi.util import get_remote_address

from core.config import settings
from core.current_user import CurrentUser


product_router_v1 = APIRouter()
product_service: ProductService = ProductService()
current_user = CurrentUser()
limiter = Limiter(key_func=get_remote_address)


@product_router_v1.post(
    "/",
    summary="Criar um novo produto",
    description="Retorna um novo produto cadastrado com sucesso",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def store(
    request: Request,
    productCreateRequestDTO: ProductCreateRequestDTO,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> ProductResponseDTO:
    return await product_service.store_service(productCreateRequestDTO)


@product_router_v1.get(
    "/{id}",
    summary="Informações do produto por ID",
    description="Retorna as informações do produto por ID",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
async def show(
    id: str, 
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> ProductResponseDTO:
    return await product_service.show_service(id)


@product_router_v1.get(
    "/",
    summary="Lista de produtos cadastrados",
    description="Retorna uma liste de produtos cadastrados",
    status_code=status.HTTP_200_OK,
    response_model=Page[ProductResponseDTO],
    responses={
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
async def index(
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> Page[ProductResponseDTO]:
    products: List[ProductResponseDTO] = await product_service.index_service()
    return paginate(products)


@product_router_v1.get(
    "/category/{category_id}",
    summary="Lista de produtos cadastrados por categoria",
    description="Retorna uma liste de produtos cadastrados por categoria",
    status_code=status.HTTP_200_OK,
    response_model=Page[ProductResponseDTO],
    responses={
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
async def index_by_category(
    category_id: str,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> Page[ProductResponseDTO]:
    products: List[ProductResponseDTO] = await product_service.index_by_category_service(category_id)
    return paginate(products)


@product_router_v1.put(
    "/{id}",
    summary="Atualizar informações de um produto por ID",
    description="Retorna as informações de um produto por ID atualizado com sucesso",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def update(
    request: Request,
    id: str,
    productUpdateRequestDTO: ProductUpdateRequestDTO,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> ProductResponseDTO:
    return await product_service.update_service(id, productUpdateRequestDTO)


@product_router_v1.patch(
    "/{id}",
    summary="Atualizar imagem de um produto por ID",
    description="Retorna a imagem de um produto por ID atualizado com sucesso",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ProductResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        406: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def upload(
    request: Request,
    id: str,
    banner: UploadFile,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> ProductResponseDTO:
    return await product_service.upload_service(id, banner)


@product_router_v1.get(
    "/file/{id}",
    summary="Imagem de um produto por ID",
    description="Retorna uma imagem de um produto por ID",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {"image/png;image/jpg;image/jpeg": {}},
            "description": "Retorna a imagem de um produto",
        },
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
async def show_file(id: str, user_logged: UserResponseDTO = Depends(current_user.get_current_user)):
    product: ProductResponseDTO = await product_service.show_service(id)
    
    return FileResponse(
        path=f"./{settings.UPLOAD_DIR}/products/{product.banner}",
        filename=product.banner
    )


@product_router_v1.delete(
    "/{id}",
    summary="Remover um produto por ID",
    description="Remove um produto específico por ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def destroy(
    request: Request,
    id: str, 
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> None:
    return await product_service.destroy_service(id)
