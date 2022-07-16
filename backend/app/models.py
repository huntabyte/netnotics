"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""

import uuid
from dataclasses import dataclass, field

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

Base = registry()


@Base.mapped
@dataclass
class User:
    __tablename__ = "users"
    __sa_dataclass_metadata_key__ = "sa"

    id: uuid.UUID = field(
        init=False,
        default_factory=uuid.uuid4,
        metadata={"sa": Column(UUID(as_uuid=True), primary_key=True)},
    )
    email: str = field(
        metadata={"sa": Column(String(254), nullable=False, unique=True, index=True)}
    )
    name: str = field(metadata={"sa": Column(String(255))})
    hashed_password: str = field(metadata={"sa": Column(String(128), nullable=False)})


@Base.mapped
@dataclass
class UserSession:
    __tablename__ = "user_sessions"
    __sa_dataclass_metadata_key__ = "sa"

    id: uuid.UUID = field(
        init=False,
        default_factory=uuid.uuid4,
        metadata={"sa": Column(UUID(as_uuid=True), primary_key=True)},
    )
    user_id: uuid.UUID = field(
        metadata={"sa": Column(ForeignKey("users.id", ondelete="CASCADE"))}
    )
    expires_at: int = field(metadata={"sa": Column(Integer, nullable=False)})


@Base.mapped
@dataclass
class Device:
    __tablename__ = "devices"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    user_id: uuid.UUID = field(
        metadata={"sa": Column(ForeignKey("users.id", ondelete="CASCADE"))}
    )
    name: str = field(metadata={"sa": Column(String(255), nullable=False)})
    ip_address: str = field(metadata={"sa": Column(String(128), nullable=False)})
