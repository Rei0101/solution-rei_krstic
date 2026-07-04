import pytest


@pytest.mark.asyncio
async def test_get_tickets(client):
    response = await client.get("/tickets")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)

@pytest.mark.asyncio
async def test_create_ticket(client):

    payload = {
        "title": "Test ticket",
        "status": "open",
        "priority": "low",
        "description": "Testing",
        "assignee": "john",
    }

    response = await client.post("/tickets", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["status"] == payload["status"]
    assert data["priority"] == payload["priority"]