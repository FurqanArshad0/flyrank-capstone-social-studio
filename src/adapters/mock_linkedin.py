from src.adapters.base import SocialPublisher, PublishResult
from src.models import Variant

class MockLinkedInPublisher(SocialPublisher):
    """Mock adapter for LinkedIn — records to database."""
    
    def get_platform_name(self) -> str:
        return "mock_linkedin"
    
    def publish(self, variant: Variant, idempotency_key: str) -> PublishResult:
        return PublishResult(
            success=True,
            message=f"Mock post to LinkedIn would be: {variant.caption[:100]}...",
            data={
                "platform": "linkedin",
                "idempotency_key": idempotency_key,
                "simulated": True
            }
        )