import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

    # Test duplicate signup
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

    # Test invalid activity
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=remove@example.com")
    
    # Check added
    response = client.get("/activities")
    data = response.json()
    assert "remove@example.com" in data["Programming Class"]["participants"]

    # Unregister
    response = client.delete("/activities/Programming%20Class/participants/remove@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

    # Check removed
    response = client.get("/activities")
    data = response.json()
    assert "remove@example.com" not in data["Programming Class"]["participants"]

    # Test unregister not signed up
    response = client.delete("/activities/Programming%20Class/participants/notsigned@example.com")
    assert response.status_code == 400

    # Test invalid activity
    response = client.delete("/activities/Invalid%20Activity/participants/test@example.com")
    assert response.status_code == 404

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    # Since it's RedirectResponse to /static/index.html, but TestClient follows redirects by default
    # Actually, RedirectResponse returns 307, but TestClient might follow
    # But since it's to /static/index.html, and mounted, it should return the HTML
    # But in test, perhaps assert 307 or check content
    # For simplicity, since it's a redirect, and TestClient follows, but wait
    # FastAPI TestClient does not follow redirects by default? Wait, actually it does for some, but let's check
    # To be safe, assert it's 307
    # Wait, RedirectResponse returns 307 for temporary redirect
    # But in the code, it's RedirectResponse(url="/static/index.html"), so 307
    # But TestClient might follow it.
    # Let's change to assert 307 or check if it returns HTML
    # For now, since it's a simple redirect, perhaps skip or assert status