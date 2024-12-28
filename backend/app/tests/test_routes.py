import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/register", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_login_user(client):
    # Register user first
    await client.post("/register", json={"username": "testuser", "password": "password123"})

    # Test login
    response = await client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_upload_document(client):
    # Register and login to get token
    await client.post("/register", json={"username": "testuser", "password": "password123"})
    login_response = await client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    # Test protected endpoint with token
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/upload_document", json={
        "subject_id": 1,
        "title": "Test Document",
        "author": "Author",
        "doc_type": "PDF",
        "summary": "Test summary",
        "content_url": "http://example.com/doc.pdf"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Document uploaded successfully"

