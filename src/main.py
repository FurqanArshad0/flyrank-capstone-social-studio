from fastapi import FastAPI
from src.database import engine, Base
from src.routes import campaigns, variants
from dotenv import load_dotenv
import os
import threading

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media Studio", version="1.0.0")

# Include routers
app.include_router(campaigns.router)
app.include_router(variants.router)

# ===== Scheduler Integration =====
# Import the scheduler worker
from src.scheduler.worker import start_scheduler

def start_background_scheduler():
    """Start the scheduler in a background thread."""
    # Run scheduler in a separate thread so it doesn't block the API
    thread = threading.Thread(target=start_scheduler, args=(30,), daemon=True)
    thread.start()
    print("🔄 Background scheduler started (checking every 30 seconds)")

# Start the scheduler automatically when the app starts
# You can comment this line out if you want to run the scheduler separately
start_background_scheduler()

# ===== Debug Endpoints =====

@app.get("/")
def root():
    return {"message": "Social Media Studio is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug/env")
def debug_env():
    """Debug endpoint to check if .env is loaded."""
    return {
        "discord_webhook_url": os.getenv("DISCORD_WEBHOOK_URL", "NOT SET"),
        "env_file_exists": os.path.exists(".env")
    }