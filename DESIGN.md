# Social Media Studio — Design Document

## Problem
Marketing teams spend hours manually posting the same content to different social platforms. This is slow, error-prone, and doesn't scale.

## Solution
A system that takes one blog post and generates platform-specific variants, lets a person approve them, and schedules them to publish — with no duplicate posts even if something fails.

## Data Models

### Campaign
- id: integer (primary key)
- title: string
- source_url: string (optional)
- source_text: text
- status: enum (draft, active, completed)
- created_at: datetime
- updated_at: datetime

### Variant
- id: integer (primary key)
- campaign_id: foreign key (Campaign)
- platform: enum (instagram, x, linkedin)
- caption: text
- image_url: string (optional)
- status: enum (draft, approved, rejected, published)
- scheduled_at: datetime (optional)
- published_at: datetime (optional)
- created_at: datetime
- updated_at: datetime

### PublishLog
- id: integer (primary key)
- variant_id: foreign key (Variant)
- platform: string
- idempotency_key: string (unique)
- status: enum (pending, success, failed)
- response: text (optional)
- created_at: datetime

## Platform Constraints

### Instagram
- Max length: 2200 characters
- Tone: visual, engaging, hashtags
- Image: 1080x1080 (square)

### X (Twitter)
- Max length: 280 characters
- Tone: concise, punchy
- Image: 1600x900 (16:9)

### LinkedIn
- Max length: 3000 characters
- Tone: professional, thought leadership
- Image: 1200x627 (1.91:1)

## API Endpoints

### Campaigns
- POST /campaigns — Create a campaign from a blog post
- GET /campaigns — List all campaigns
- GET /campaigns/{id} — Get campaign details

### Variants
- GET /campaigns/{id}/variants — List variants for a campaign
- PUT /variants/{id} — Update variant (caption, image)
- POST /variants/{id}/approve — Approve a variant
- POST /variants/{id}/reject — Reject a variant
- POST /variants/{id}/schedule — Schedule a variant

### Publishing
- POST /variants/{id}/publish — Publish now (idempotent)
- GET /variants/{id}/status — Get publish status
- GET /publish-logs — View publish history

## The SocialPublisher Interface

```python
class SocialPublisher:
    def publish(self, variant: Variant, idempotency_key: str) -> PublishResult:
        """Publish a variant to the platform. Idempotent by key."""
        pass
    
    def get_platform_name(self) -> str:
        """Return platform name."""
        pass