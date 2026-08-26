from abc import ABC, abstractmethod
from src.models import Variant

class PublishResult:
    """Result of a publish attempt."""
    def __init__(self, success: bool, message: str = "", data: dict = None):
        self.success = success
        self.message = message
        self.data = data or {}

class SocialPublisher(ABC):
    """Interface for all platform adapters."""
    
    @abstractmethod
    def publish(self, variant: Variant, idempotency_key: str) -> PublishResult:
        """Publish a variant to the platform. Must be idempotent."""
        pass
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Return the platform name (e.g., 'telegram', 'mock_x')."""
        pass