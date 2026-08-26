from fastapi import FastAPI
from src.database import engine, Base
from src.routes import campaigns, variants
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media Studio", version="1.0.0")

app.include_router(campaigns.router)
app.include_router(variants.router)

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