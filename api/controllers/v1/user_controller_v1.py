from fastapi import APIRouter, status, Request, Depends, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm

from slowapi import Limiter
from slowapi.util import get_remote_address

from api.services.user_service import UserService
from api.dtos.responses.user_response_dto import (
    UserResponseDTO,
    TokenResponseDTO
)
from api.dtos.responses.exception_response_dto import (
    ExceptionResponseDTO,
    ExceptionRateLimitResponseDTO
)
from api.dtos.requests.user_request_dto import (
    UserCreateRequestDTO,
    UserLoginRequestDTO,
    UserUpdateRequestDTO,
    UserUpdatePassRequestDTO
)

from core.config import settings
from core.auth import Auth
from core.current_user import CurrentUser


user_router_v1 = APIRouter()
auth_config = Auth()
user_service: UserService = UserService()
current_user: CurrentUser = CurrentUser()
limiter = Limiter(key_func=get_remote_address)


@user_router_v1.post(
    "/signup",
    summary="Criar um novo usuário",
    description="Retorna um novo usuário com sucesso",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        409: {"model": ExceptionResponseDTO},
    }
)
async def signup(
    userCreateRequestDTO: UserCreateRequestDTO
) -> UserResponseDTO:
    return await user_service.signup_service(userCreateRequestDTO)


@user_router_v1.post(
    "/signin",
    summary="Login do usuário",
    description="Retorna um token de acesso com sucesso",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES_AUTH) + "/minute")
async def signin(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
) -> TokenResponseDTO:
    userLoginRequest: UserLoginRequestDTO = UserLoginRequestDTO(
        email=form_data.username,
        password=form_data.password
    )

    user: UserResponseDTO = await user_service.signin_service(userLoginRequest)

    return JSONResponse(
        content={
            "access_token": auth_config.create_token_access(sub=user.id),
            "token_type": "bearer"
        },
        status_code=status.HTTP_200_OK
    )


@user_router_v1.get(
    "/me",
    summary="Informações do usuário logado",
    description="Retorna as informações do usuário logado",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        401: {"model": ExceptionResponseDTO},
    }
)
async def me(
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> UserResponseDTO:
    return user_logged


@user_router_v1.put(
    "/update",
    summary="Atualizar informações do usuário",
    description="Retorna as informações do usuário atualizado",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def update(
    request: Request,
    userUpdateRequestDTO: UserUpdateRequestDTO,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> UserResponseDTO:
    return await user_service.update_service(user_logged.id, userUpdateRequestDTO)


@user_router_v1.put(
    "/reset-password",
    summary="Atualizar a senha do usuário",
    description="Retorna a senha atualizada do usuário",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponseDTO,
    responses={
        400: {"model": ExceptionResponseDTO},
        401: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def update_password(
    request: Request,
    userUpdatePassRequestDTO: UserUpdatePassRequestDTO,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> UserResponseDTO:
    return await user_service.update_password_service(
        user_logged.id, 
        userUpdatePassRequestDTO
    )


@user_router_v1.patch(
    "/",
    summary="Atualizar o avatar do usuário",
    description="Retorna o avatar atualizado do usuário",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponseDTO,
    responses={
        401: {"model": ExceptionResponseDTO},
        406: {"model": ExceptionResponseDTO},
        429: {"model": ExceptionRateLimitResponseDTO}
    }
)
@limiter.limit(str(settings.REQUEST_PER_MINUTES) + "/minute")
async def upload(
    request: Request,
    avatar: UploadFile,
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
) -> UserResponseDTO:
    return await user_service.upload_service(user_logged, avatar)


@user_router_v1.get(
    "/file",
    summary="Avatar do usuário logado",
    description="Retorna o avatar de um usuário logado",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ExceptionResponseDTO},
        401: {"model": ExceptionResponseDTO}
    }
)
async def file(
    user_logged: UserResponseDTO = Depends(current_user.get_current_user)
):
    return FileResponse(
        path=f"./{settings.UPLOAD_DIR}/users/{user_logged.avatar}",
        filename=user_logged.avatar
    )
    