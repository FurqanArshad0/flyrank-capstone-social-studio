from src.adapters.base import SocialPublisher, PublishResult
from src.models import Variant

class MockXPublisher(SocialPublisher):
    """Mock adapter for X (Twitter) — records to database."""
    
    def get_platform_name(self) -> str:
        return "mock_x"
    
    def publish(self, variant: Variant, idempotency_key: str) -> PublishResult:
        return PublishResult(
            success=True,
            message=f"Mock post to X would be: {variant.caption[:100]}...",
            data={
                "platform": "x",
                "idempotency_key": idempotency_key,
                "simulated": True
            }
        )