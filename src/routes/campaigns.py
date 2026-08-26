from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from src.database import get_db
from src.models import Campaign, Variant, Platform, VariantStatus
from src.services import generator

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

# --- Pydantic schemas ---

class CampaignCreate(BaseModel):
    title: str
    source_url: Optional[str] = None
    source_text: str

class CampaignResponse(BaseModel):
    id: int
    title: str
    source_url: Optional[str]
    source_text: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VariantResponse(BaseModel):
    id: int
    campaign_id: int
    platform: str
    caption: str
    image_url: Optional[str]
    status: str
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.post("/", response_model=CampaignResponse)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    """Ingest a blog post and create a campaign."""
    
    # 1. Create the campaign
    new_campaign = Campaign(
        title=campaign.title,
        source_url=campaign.source_url,
        source_text=campaign.source_text,
        status="draft"
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    
    # 2. Generate variants for each platform
    platforms = [Platform.INSTAGRAM, Platform.X, Platform.LINKEDIN]
    
    for platform in platforms:
        caption = generator.generate_caption(campaign.source_text, platform)
        variant = Variant(
            campaign_id=new_campaign.id,
            platform=platform,
            caption=caption,
            status=VariantStatus.DRAFT
        )
        db.add(variant)
    
    db.commit()
    db.refresh(new_campaign)
    
    return new_campaign

@router.get("/", response_model=list[CampaignResponse])
def list_campaigns(db: Session = Depends(get_db)):
    """List all campaigns."""
    return db.query(Campaign).all()

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a single campaign by ID."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.get("/{campaign_id}/variants", response_model=list[VariantResponse])
def get_campaign_variants(campaign_id: int, db: Session = Depends(get_db)):
    """Get all variants for a campaign."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign.variants