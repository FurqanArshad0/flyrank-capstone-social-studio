import os
import requests
from src.adapters.base import SocialPublisher, PublishResult
from src.models import Variant

class DiscordPublisher(SocialPublisher):
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    def get_platform_name(self) -> str:
        return "discord"
    
    def publish(self, variant: Variant, idempotency_key: str) -> PublishResult:
        if not self.webhook_url:
            return PublishResult(False, "Discord webhook URL not configured")
        
        # Prepare the message
        caption = variant.caption[:200] if variant.caption else "No caption"
        content = f"📢 **{caption}**"
        
        # Send the request
        try:
            response = requests.post(
                self.webhook_url,
                json={"content": content},
                timeout=30
            )
            
            # Check if the request was successful
            if response.status_code == 204:
                # Discord webhooks return 204 No Content on success
                return PublishResult(
                    success=True,
                    message="Message sent to Discord",
                    data={"status_code": 204}
                )
            elif response.status_code == 200:
                # Some webhook endpoints return 200 with JSON
                return PublishResult(
                    success=True,
                    message="Message sent to Discord",
                    data=response.json() if response.text else {}
                )
            else:
                # Any other status code is an error
                return PublishResult(
                    success=False,
                    message=f"Discord returned status {response.status_code}: {response.text[:100]}"
                )
                
        except requests.exceptions.Timeout:
            return PublishResult(False, "Discord request timed out after 30 seconds")
        except requests.exceptions.ConnectionError:
            return PublishResult(False, "Could not connect to Discord")
        except Exception as e:
            return PublishResult(False, f"Discord error: {str(e)}")