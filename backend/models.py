import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class StatusCheck(Base):
    __tablename__ = "status_checks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    client_name = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=utcnow)
