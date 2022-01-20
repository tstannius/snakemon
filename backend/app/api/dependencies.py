"""FastAPI dependencies

FastAPI uses dependencies in it's routes to provide various functionality,
e.g. authentication, database connection, etc.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator, Optional

from app.db import schemas
from app.db.models import User
from app.db.session import async_session
from app.core.config import settings
from app.core.oauth2 import OAuth2PasswordBearerWithCookie

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

reusable_oauth2_cookie = OAuth2PasswordBearerWithCookie(tokenUrl="auth/access-token")
# reusable_oauth2_request = OAuth2PasswordBearer(tokenUrl="auth/access-token") # TODO: reimplement token auth

async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2_cookie)
) -> User:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user: Optional[User] = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
