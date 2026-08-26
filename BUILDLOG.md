# Build Log — Social Media Studio

## AI Usage

### Where AI Helped

1. **Database models** — Generated initial `models.py` structure
2. **FastAPI routes** — Created CRUD endpoints for campaigns and variants
3. **Discord adapter** — Built the `DiscordPublisher` class
4. **Scheduler** — Set up the background worker

### Where AI Was Wrong

1. **Import paths** — Multiple import errors needed manual fixes
2. **`.env` loading** — Initially forgot `load_dotenv()` in `main.py`
3. **Publisher mapping** — `instagram` platform needed to map to Discord

### What I Changed

1. Fixed import statements to match project structure
2. Added `load_dotenv()` to read environment variables
3. Updated `get_publisher()` to map `instagram` → `DiscordPublisher`
4. Added proper error handling for Discord responses

### Files Written by Hand

- `src/adapters/base.py` — Interface design
- `src/routes/variants.py` — Review workflow logic
- `src/scheduler/worker.py` — Background scheduler
- `src/models.py` — Database schema

### Files Generated with AI Help

- `src/adapters/discord.py` — Discord webhook adapter
- `src/routes/campaigns.py` — Campaign CRUD endpoints
- `src/main.py` — Server setup

## Lessons Learned

1. `.env` must be loaded before any other imports
2. Platform names in database must match publisher mapping
3. Discord webhooks return 204 No Content on success
4. Idempotency keys must be consistent across retries