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