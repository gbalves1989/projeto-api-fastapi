from core.config import settings

from datetime import datetime, timedelta

from pytz import timezone

from jose import jwt


class Auth:
    def _create_token(self, type_token: str, time_life: timedelta, sub: str) -> str:
        payload = {}

        sp = timezone("America/Sao_Paulo")
        expire_in = datetime.now(tz=sp) + time_life

        payload["type"] = type_token
        payload["exp"] = expire_in
        payload["iat"] = datetime.now(tz=sp)
        payload["sub"] = str(sub)

        return jwt.encode(
            payload, 
            key=settings.JWT_SECRET, 
            algorithm=settings.ALGORITHM
        )

    def create_token_access(self, sub: str) -> str:
        return self._create_token(
            type_token="access_token",
            time_life=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            sub=sub
        )
        