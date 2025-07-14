from fastapi import APIRouter, status, Depends, Request
from fastapi_pagination import Page, paginate

from api.dtos.responses.category_response_dto import CategoryResponseDTO
from api.dtos.responses.exception_response_dto import (
    ExceptionResponseDTO,
    ExceptionRateLimitResponseDTO
)
from api.dtos.requests.category_request_dto import (
    CategoryCreateRequestDTO,
    CategoryUpdateRequestDTO
)
from api.services.category_service import CategoryService
from api.dtos.responses.user_response_dto import UserResponseDTO

from typing import List

from slowapi import Limiter
from slowapi.util import get_remote_address 

from core.current_user import CurrentUser
from core.config import settings


category_router_v1 = APIRouter()
category_service = CategoryService()
current_user = CurrentUser()
limiter = Limiter(key_func=get_remote_address)


@category_router_v1.post(
    "/",
    summary="Cadastrar uma nova categoria",
    description="Retorna uma nova categoria com sucesso",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def store(
    request: Request,
    categoryCreateRequestDTO: CategoryCreateRequestDTO,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> CategoryResponseDTO:
    return await category_service.store_service(user_logged.id, categoryCreateRequestDTO)


@category_router_v1.get(
    "/",
    summary="Lista de categorias por usuário",
    description="Retorna uma lista de categorias por usuário",
    status_code=status.HTTP_200_OK,
    response_model=Page[CategoryResponseDTO],
    responses={
        401: {"model": ExceptionResponseDTO}
    }
)
async def index(
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> Page[CategoryResponseDTO]:
    categories: List[CategoryResponseDTO] = await category_service.index_service(user_logged.id)
    return paginate(categories)


@category_router_v1.get(
    "/{id}",
    summary="Informações de uma categoria específica por ID",
    description="Retorna informações de uma categoria específica por ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO}
    }
)
async def show(
    id: str,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> CategoryResponseDTO:
    return await category_service.show_service(id)


@category_router_v1.put(
    "/{id}",
    summary="Atualizar informações de uma categoria por ID",
    description="Retorna uma categoria com as informações atualizadas",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CategoryResponseDTO,
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
    categoryUpdateRequestDTO: CategoryUpdateRequestDTO,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> CategoryResponseDTO:
    return await category_service.update_service(id, categoryUpdateRequestDTO)


@category_router_v1.delete(
    "/{id}",
    summary="Remover uma categoria por ID",
    description="Remove uma categoria específica por ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ExceptionResponseDTO},
        404: {"model": ExceptionResponseDTO},
        422: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def destroy(
    request: Request, 
    id: str,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> None:
    return await category_service.destroy_service(id)
