from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    ip_address = Column(String, index=True)
    username = Column(String)
    hashed_password = Column(String)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="devices")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
