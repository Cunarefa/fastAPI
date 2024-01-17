from datetime import timedelta

from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from src.config import SECRET_KEY


class Settings(BaseModel):
    authjwt_secret_key: str = f"{SECRET_KEY}"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires: int = timedelta(minutes=15)
    refresh_expires: int = timedelta(days=30)


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
