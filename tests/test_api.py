import sys
import os

# Add the parent directory to the path so we can import src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_campaign():
    """Test creating a campaign."""
    response = client.post(
        "/campaigns/",
        json={"title": "Test Campaign", "source_text": "Test content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Campaign"
    assert data["status"] == "draft"

def test_get_campaigns():
    """Test listing campaigns."""
    response = client.get("/campaigns/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_variant_workflow():
    """Test the full workflow: create → approve → publish."""
    # Create campaign
    response = client.post(
        "/campaigns/",
        json={"title": "Workflow Test", "source_text": "Test content for workflow"}
    )
    assert response.status_code == 200
    campaign_id = response.json()["id"]
    
    # Get variants
    response = client.get(f"/campaigns/{campaign_id}/variants")
    assert response.status_code == 200
    variants = response.json()
    assert len(variants) >= 1
    variant_id = variants[0]["id"]
    
    # Approve variant
    response = client.post(f"/variants/{variant_id}/approve")
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    
    # Publish variant
    response = client.post(f"/variants/{variant_id}/publish")
    assert response.status_code == 200
    data = response.json()
    assert "idempotency_key" in data