from fastapi import FastAPI
from src.database import engine, Base
from src.routes import campaigns, variants

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