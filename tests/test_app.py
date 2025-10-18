import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

ACTIVITY = "Chess Club"
EMAIL = "pytestuser@mergington.edu"


def test_signup_new_participant():
    # Remove if present
    client.delete(f"/activities/{ACTIVITY}/participants?email={EMAIL}")
    # Sign up
    response = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    # Check participant is present
    activities = client.get("/activities").json()
    assert EMAIL in activities[ACTIVITY]["participants"]

def test_signup_duplicate():
    # Sign up once
    client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    # Try duplicate
    response = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_unregister_participant():
    # Ensure present
    client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    # Unregister
    response = client.delete(f"/activities/{ACTIVITY}/participants?email={EMAIL}")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    # Check participant is gone
    activities = client.get("/activities").json()
    assert EMAIL not in activities[ACTIVITY]["participants"]

def test_unregister_nonexistent():
    # Remove if present
    client.delete(f"/activities/{ACTIVITY}/participants?email={EMAIL}")
    # Try to unregister again
    response = client.delete(f"/activities/{ACTIVITY}/participants?email={EMAIL}")
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]
