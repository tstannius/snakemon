"""
Put here any code that must be run before application startup

Note that the script must be run as a library module for imports to work
cd backend
python3 -m app.init_app

By defualt `main` creates a superuser if not exists
"""
import asyncio
import logging

from app.core import security
from app.core.config import settings
from app.db.models import User
from app.db.session import async_session

async def main() -> None:
    print("Create initial data")
    async with async_session() as session:
        # add test user if dev env
        if (settings.ENVIRONMENT == "DEV"):
            logging.warning("[WARNING]: Dev environment detected. Creating dev data.")
            new_user = User(
                email="john.doe@snakemon.org",
                username="jd",
                hashed_password=security.get_password_hash("jd"),
            )
            session.add(new_user)
            await session.commit()

    print("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
