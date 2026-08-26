import os
import time
import threading
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Variant, VariantStatus, PublishLog, PublishStatus
from src.routes.variants import get_publisher
import hashlib

DATABASE_URL = "sqlite:///./social.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def publish_due_variants():
    """Check for variants that are due to be published and publish them."""
    db = SessionLocal()
    
    try:
        # Find variants that are approved and have a scheduled time in the past
        now = datetime.utcnow()
        due_variants = db.query(Variant).filter(
            Variant.status == VariantStatus.APPROVED,
            Variant.scheduled_at <= now,
            Variant.published_at == None
        ).all()
        
        for variant in due_variants:
            print(f"Publishing scheduled variant {variant.id}...")
            
            # Create idempotency key
            idempotency_key = hashlib.sha256(
                f"{variant.id}:{variant.platform}".encode()
            ).hexdigest()
            
            # Check if already published
            existing_log = db.query(PublishLog).filter(
                PublishLog.idempotency_key == idempotency_key
            ).first()
            
            if existing_log:
                print(f"  ⏭️  Variant {variant.id} already published (idempotency)")
                continue
            
            # Get publisher and publish
            platform_name = variant.platform.value
            publisher = get_publisher(platform_name)
            result = publisher.publish(variant, idempotency_key)
            
            # Log the attempt
            log = PublishLog(
                variant_id=variant.id,
                platform=variant.platform,
                idempotency_key=idempotency_key,
                status=PublishStatus.SUCCESS if result.success else PublishStatus.FAILED,
                response=result.message
            )
            db.add(log)
            
            # Update variant status
            if result.success:
                variant.status = VariantStatus.PUBLISHED
                variant.published_at = datetime.utcnow()
                print(f"   Variant {variant.id} published successfully!")
            else:
                print(f"   Variant {variant.id} failed: {result.message}")
            
            db.commit()
    
    except Exception as e:
        print(f" Scheduler error: {e}")
    finally:
        db.close()

def start_scheduler(interval_seconds: int = 30):
    """Start the background scheduler that checks for due variants."""
    print(f"🔄 Scheduler started — checking every {interval_seconds} seconds")
    
    while True:
        try:
            publish_due_variants()
        except Exception as e:
            print(f" Scheduler error: {e}")
        
        time.sleep(interval_seconds)

def run_scheduler_once():
    """Run the scheduler once (for testing)."""
    publish_due_variants()

if __name__ == "__main__":
    # When run directly, start the infinite loop
    start_scheduler()