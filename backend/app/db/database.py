from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/snakemon.db" # TODO: get from settings
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# check_same_thread only needed for sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
