# Social Media Studio

Turn one blog post into a full social media campaign — scheduled, approved, and published reliably.

## What It Does

1. **Ingest** – Accept a blog post (URL or pasted text)
2. **Generate** – Create platform-specific variants (Instagram, X, LinkedIn style)
3. **Review** – Approve or reject each variant before it goes live
4. **Schedule** – Set a publish time for approved variants
5. **Publish** – Automatically publish to a real platform (Discord) or simulate others

## How It Works
Blog Post → Campaign → Variants → Review → Schedule → Publish



## Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **Discord** | ✅ Real | Published via webhook |
| **X (Twitter)** | 🧪 Mock | Architecture-ready |
| **LinkedIn** | 🧪 Mock | Architecture-ready |

The system is designed with adapters — adding a real platform only requires writing a new adapter, without changing the core logic.

## Quick Start

```bash
# Clone and install
git clone https://github.com/FurqanArshad0/flyrank-capstone-social-studio.git
cd flyrank-capstone-social-studio
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up secrets
cp .env.example .env
# Add your DISCORD_WEBHOOK_URL to .env

# Run the server
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
Example API Flow
bash
# 1. Create a campaign
curl -X POST http://localhost:8000/campaigns/ -H "Content-Type: application/json" -d '{"title": "Hello", "source_text": "Content"}'

# 2. Approve a variant
curl -X POST http://localhost:8000/variants/1/approve

# 3. Publish to Discord
curl -X POST http://localhost:8000/variants/1/publish

# 4. Test idempotency (duplicate prevented)
curl -X POST http://localhost:8000/variants/1/publish
Key Feature: Idempotency
A retry never creates a duplicate post. Try it yourself:

First publish ✅ → succeeds

Second publish ❌ → returns "Already published"

Architecture
The system uses the adapter pattern:

text
SocialPublisher (interface)
    ├── DiscordPublisher   → real webhook
    ├── MockXPublisher     → simulation
    └── MockLinkedInPublisher → simulation
Built With
Python 3.10+

FastAPI

SQLite

Discord Webhooks

APScheduler

Lessons Learned
Idempotency is critical for reliable publishing

The adapter pattern keeps the system extensible

Tests prove the system works under retry scenarios

License
MIT

