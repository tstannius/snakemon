from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from app.api import dependencies as deps
from app.core import security
from app.core.config import settings
from app.db import schemas
from app.db.models import User

router = APIRouter()

@router.post("/access-token")
async def login_access_token(
    response: Response,
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token, get an access token for future requests using username and password
    """
    result = await session.execute(select(User).where(User.username == form_data.username))
    user: Optional[User] = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not security.verify_password(form_data.password, user.hashed_password):  # type: ignore
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token, expire_at = security.create_access_token(user.id)
    # refresh_token, refresh_expire_at = security.create_refresh_token(user.id)
    
    response.set_cookie(key="access_token", 
                        value=f"Bearer {access_token}", 
                        httponly=True, 
                        secure=True, 
                        samesite="lax") # TODO: check args
    
    return {"message": "Success"}


@router.post("/delete-token", status_code=status.HTTP_200_OK)
async def logout(
    response: Response, 
    current_user: User = Depends(deps.get_current_user)):
    response.delete_cookie("access_token")
    return {"message": "Success"}


@router.post("/test-token", response_model=schemas.User)
async def test_token(current_user: User = Depends(deps.get_current_user)):
    """
    Test access token for current user
    """
    return current_user


@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_token(
    input: schemas.TokenRefresh, session: AsyncSession = Depends(deps.get_session)
):
    """
    OAuth2 compatible token, get an access token for future requests using refresh token
    """
    try:
        payload = jwt.decode(
            input.refresh_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    result = await session.execute(select(User).where(User.id == token_data.sub))
    user: Optional[User] = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    access_token, expire_at = security.create_access_token(user.id)
    refresh_token, refresh_expire_at = security.create_refresh_token(user.id)
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
        "refresh_token": refresh_token,
        "refresh_expire_at": refresh_expire_at,
    }
