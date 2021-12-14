from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from app.core.config import settings

SQLALCHEMY_DATABASE_URI = settings.DEFAULT_SQLALCHEMY_DATABASE_URI

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, connect_args={"check_same_thread": False})
async_session = sessionmaker(bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)
