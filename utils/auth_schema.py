from fastapi.security import OAuth2PasswordBearer

from core.auth import settings


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VERSION}/users/signin"
)
