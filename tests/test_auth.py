import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post("/register", json={"username": "testuser", "password": "test123"})
    assert response.status_code == 200

def test_login(client):
    response = client.post("/login", json={"username": "testuser", "password": "test123"})
    assert response.status_code == 200
    assert b"Login successful" in response.data

def test_protected_route(client):
    client.post("/login", json={"username": "testuser", "password": "test123"})
    response = client.get("/dashboard")
    assert response.status_code == 200

def test_logout(client):
    client.post("/login", json={"username": "testuser", "password": "test123"})
    response = client.get("/logout")
    assert response.status_code == 200
