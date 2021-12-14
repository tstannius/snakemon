"""FastAPI dependencies

FastAPI uses dependencies in it's routes to provide various functionality,
e.g. authentication, database connection, etc.
"""
from app.db.session import async_session
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
