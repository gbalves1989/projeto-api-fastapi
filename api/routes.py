from fastapi import APIRouter

from api.controllers.v1 import (
    user_controller_v1,
    category_controller_v1,
    product_controller_v1
)

from core.config import settings


api_router = APIRouter()

if settings.API_VERSION == "v1":
    api_router.include_router(
        user_controller_v1.user_router_v1,
        prefix="/users",
        tags=["Users"]
    )
    api_router.include_router(
        category_controller_v1.category_router_v1,
        prefix="/categories",
        tags=["Categories"]
    )
    api_router.include_router(
        product_controller_v1.product_router_v1,
        prefix="/products",
        tags=["Products"]
    )
    