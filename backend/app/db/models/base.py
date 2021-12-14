from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # TODO: consider making django-like table name
        # Alembic and FastAPI will still know what to do
        return cls.__name__.lower()
