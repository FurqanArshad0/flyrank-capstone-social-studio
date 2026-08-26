from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from src.database import get_db
from src.models import Variant, VariantStatus

router = APIRouter(prefix="/variants", tags=["variants"])

class VariantUpdate(BaseModel):
    caption: str

class VariantStatusUpdate(BaseModel):
    status: str

@router.get("/{variant_id}")
def get_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant

@router.put("/{variant_id}")
def update_variant(variant_id: int, update: VariantUpdate, db: Session = Depends(get_db)):
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    variant.caption = update.caption
    variant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(variant)
    return variant

@router.post("/{variant_id}/approve")
def approve_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    variant.status = VariantStatus.APPROVED
    variant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(variant)
    return {"message": "Variant approved", "status": variant.status}

@router.post("/{variant_id}/reject")
def reject_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    variant.status = VariantStatus.REJECTED
    variant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(variant)
    return {"message": "Variant rejected", "status": variant.status}
from pydantic import BaseModel
from datetime import datetime

class ScheduleRequest(BaseModel):
    scheduled_at: datetime

@router.post("/{variant_id}/schedule")
def schedule_variant(variant_id: int, request: ScheduleRequest, db: Session = Depends(get_db)):
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    
    # Rule: Only approved variants can be scheduled
    if variant.status != VariantStatus.APPROVED:
        raise HTTPException(
            status_code=403, 
            detail=f"Cannot schedule variant with status '{variant.status}'. Only approved variants can be scheduled."
        )
    
    variant.scheduled_at = request.scheduled_at
    variant.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(variant)
    
    return {"message": f"Variant scheduled for {request.scheduled_at}", "variant": variant}


import hashlib
from datetime import datetime
from src.models import PublishLog, PublishStatus, VariantStatus
from src.adapters.discord import DiscordPublisher
from src.adapters.mock_x import MockXPublisher
from src.adapters.mock_linkedin import MockLinkedInPublisher

# Publisher factory
def get_publisher(platform: str):
    """Return the correct publisher for a platform."""
    platform_map = {
        "instagram": DiscordPublisher,      # Use Discord for Instagram
        "x": MockXPublisher,                # Mock for X
        "linkedin": MockLinkedInPublisher,  # Mock for LinkedIn
        "discord": DiscordPublisher,        # Direct Discord
        "mock_x": MockXPublisher,
        "mock_linkedin": MockLinkedInPublisher,
    }
    publisher_class = platform_map.get(platform)
    if not publisher_class:
        raise ValueError(f"Unknown platform: {platform}")
    return publisher_class()
@router.post("/{variant_id}/publish")
def publish_variant(variant_id: int, db: Session = Depends(get_db)):
    """Publish a variant to its platform. Idempotent."""
    
    # 1. Get the variant
    variant = db.query(Variant).filter(Variant.id == variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    
    # 2. Check if approved
    if variant.status != VariantStatus.APPROVED:
        raise HTTPException(
            status_code=403,
            detail=f"Cannot publish variant with status '{variant.status}'. Only approved variants can be published."
        )
    
    # 3. Create idempotency key
    idempotency_key = hashlib.sha256(
        f"{variant.id}:{variant.platform}".encode()
    ).hexdigest()
    
    # 4. Check if already published
    existing_log = db.query(PublishLog).filter(
        PublishLog.idempotency_key == idempotency_key
    ).first()
    
    if existing_log:
        return {
            "message": "Already published",
            "idempotency_key": idempotency_key,
            "variant_id": variant_id,
            "platform": variant.platform.value,
            "previous_result": existing_log.response
        }
    
    # 5. Get the publisher and publish
    platform_name = variant.platform.value
    publisher = get_publisher(platform_name)
    
    result = publisher.publish(variant, idempotency_key)
    
    # 6. Log the attempt
    log = PublishLog(
        variant_id=variant.id,
        platform=variant.platform,
        idempotency_key=idempotency_key,
        status=PublishStatus.SUCCESS if result.success else PublishStatus.FAILED,
        response=result.message
    )
    db.add(log)
    
    # 7. Update variant status if successful
    if result.success:
        variant.status = VariantStatus.PUBLISHED
        variant.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(variant)
    
    return {
        "message": result.message,
        "success": result.success,
        "idempotency_key": idempotency_key,
        "variant_id": variant_id,
        "platform": variant.platform.value,
        "status": variant.status
    }

@router.get("/{variant_id}/publish-logs")
def get_publish_logs(variant_id: int, db: Session = Depends(get_db)):
    """Get all publish logs for a variant."""
    logs = db.query(PublishLog).filter(PublishLog.variant_id == variant_id).all()
    return logs