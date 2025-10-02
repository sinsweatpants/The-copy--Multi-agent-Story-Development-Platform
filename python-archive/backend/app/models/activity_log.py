import uuid
from sqlalchemy import Column, String, DateTime, func, UUID, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, INET
from sqlalchemy.orm import relationship
from .base import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    activity_type = Column(String(100), nullable=False, index=True)
    activity_description = Column(Text, nullable=True)

    activity_data = Column(JSONB, default={})

    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    session = relationship("Session", back_populates="activity_logs")
    user = relationship("User", back_populates="activity_logs")