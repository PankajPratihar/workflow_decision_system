from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class RequestDB(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False)
    payload = Column(JSON)
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    audit_logs = relationship("AuditLogDB", back_populates="request")

class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id_internal = Column(Integer, ForeignKey("requests.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    event = Column(String, nullable=False)
    details = Column(String)

    request = relationship("RequestDB", back_populates="audit_logs")

class ProcessedRequestDB(Base):
    __tablename__ = "processed_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
