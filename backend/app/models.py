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
from datetime import datetime, timezone
from dataclasses import dataclass, field

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry
from sqlalchemy.ext.hybrid import hybrid_property

from app.services.restconf import RESTCONF

Base = registry()


@dataclass
class BaseMixin:
    __sa_dataclass_metadata_key__ = "sa"

    created: timezone = field(
        init=False,
        metadata={"sa": Column(DateTime, default=datetime.utcnow())},
    )
    updated: timezone = field(
        init=False,
        metadata={"sa": Column(DateTime, default=datetime.utcnow())},
    )


@Base.mapped
@dataclass
class User(BaseMixin):
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
class Device(BaseMixin):
    __tablename__ = "devices"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    user_id: uuid.UUID = field(
        metadata={"sa": Column(ForeignKey("users.id", ondelete="CASCADE"))}
    )
    name: str = field(metadata={"sa": Column(String(255), nullable=False)})
    ip_address: str = field(
        metadata={"sa": Column(String(128), nullable=True, default=None)}
    )
    host: str = field(metadata={"sa": Column(String(255), nullable=True, default=None)})
    username: str = field(
        metadata={"sa": Column(String(255), nullable=True, default=None)}
    )
    password: str = field(
        metadata={"sa": Column(String(255), nullable=True, default=None)}
    )
    manageable: bool = field(
        metadata={"sa": Column(Boolean, nullable=False, default=False)}
    )

    @hybrid_property
    async def is_manageable(self):
        device_client = RESTCONF(
            host=self.host, username=self.username, password=self.password
        )
        result = await device_client.verify_connectivity(raiseErr=False)
        self.manageable = result
        return result
