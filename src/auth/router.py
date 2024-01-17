from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from async_fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .schemas import settings
from .services import authenticate_user, redis_conn
from src.users.schemas import UserCreate

router = APIRouter(prefix="/auth")


@router.get("/current_user")
async def user(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_required()

    current_user = await Authorize.get_jwt_subject()
    return {"user": current_user}


@router.post('/login')
async def login(user: UserCreate, session: Annotated[AsyncSession, Depends(get_session)], Authorize: AuthJWT = Depends()):
    db_user = authenticate_user(session, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Not authenticated. Bad email or password")

    access_token = await Authorize.create_access_token(subject=user.email)
    refresh_token = await Authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_refresh_token_required()

    current_user = await Authorize.get_jwt_subject()
    new_access_token = await Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.delete("/logout")
async def logout(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_required()

    jti = (await Authorize.get_raw_jwt())["jti"]
    redis_conn.setex(jti, settings.access_expires, "true")
    return {"detail": "Access token has been revoke"}


@router.delete("/refresh-revoke")
async def refresh_revoke(Authorize: AuthJWT = Depends()):
    await Authorize.jwt_refresh_token_required()

    jti = (await Authorize.get_raw_jwt())["jti"]
    redis_conn.setex(jti, settings.refresh_expires, "true")
    return {"detail": "Refresh token has been revoke"}