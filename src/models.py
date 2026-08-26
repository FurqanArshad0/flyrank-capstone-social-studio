from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base
import enum

class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"

class VariantStatus(str, enum.Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"

class Platform(str, enum.Enum):
    INSTAGRAM = "instagram"
    X = "x"
    LINKEDIN = "linkedin"

class PublishStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    source_url = Column(String(500), nullable=True)
    source_text = Column(Text, nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    variants = relationship("Variant", back_populates="campaign", cascade="all, delete-orphan")

class Variant(Base):
    __tablename__ = "variants"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    platform = Column(Enum(Platform), nullable=False)
    caption = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    status = Column(Enum(VariantStatus), default=VariantStatus.DRAFT)
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    campaign = relationship("Campaign", back_populates="variants")
    publish_logs = relationship("PublishLog", back_populates="variant", cascade="all, delete-orphan")

class PublishLog(Base):
    __tablename__ = "publish_logs"
    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=False)
    platform = Column(Enum(Platform), nullable=False)
    idempotency_key = Column(String(100), unique=True, index=True)
    status = Column(Enum(PublishStatus), default=PublishStatus.PENDING)
    response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    variant = relationship("Variant", back_populates="publish_logs")