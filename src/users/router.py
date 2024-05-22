from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.users.models import User
from src.users.schemas import UserRead, UserCreate
from src.users.services import get_password_hash

router = APIRouter(prefix="/users")


@router.get("/", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    # await Authorize.jwt_required()

    query = select(User).order_by(User.registered_at.desc())
    data = await session.execute(query)
    return data.scalars().all()


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.email == user.email)
    is_user = await session.execute(query)

    if is_user.scalar():
        raise ValueError("User already exists.")

    user.password = get_password_hash(user.password)
    stmt = insert(User).values(**user.model_dump())
    await session.execute(stmt)
    await session.commit()

    db_user = await session.execute(select(User).where(User.email == user.email))
    return db_user.scalar()


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.id == user_id)
    data = await session.execute(query)
    user = data.scalar()

    if not user:
        raise ValueError("User does not exist.")

    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully."}


@router.get("/", response_model=list[UserRead])
async def check_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # await Authorize.jwt_required()

    query = select(User).order_by(User.registered_at.desc())
    data = await session.execute(query)
    return data.scalars().all()
