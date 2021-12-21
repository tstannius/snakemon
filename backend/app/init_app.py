"""
Put here any Python code that must be runned before application startup.
It is included in `init.sh` script.

By defualt `main` create a superuser if not exists
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
            logging.warn("[WARNING]: Dev environment detected. Creating dev data.")
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
