from async_fastapi_jwt_auth import AuthJWT
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.services import verify_password

redis_conn = Redis(host="localhost", port=6379, encoding="utf8", decode_responses=True)


async def authenticate_user(session: AsyncSession, email: str, password: str):
    query = select(User).filter(User.email == email).first()
    db_user = await session.execute(query)
    if db_user.scalar() and verify_password(password, db_user.password):
        return True
    return False


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    entry = redis_conn.get(jti)
    return entry and entry == "true"
