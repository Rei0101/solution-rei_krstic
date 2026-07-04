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


@pytest.mark.asyncio
async def test_get_ticket_by_id(client):

    payload = {
        "title": "Another ticket",
        "status": "open",
        "priority": "medium",
        "description": "",
        "assignee": None,
    }

    created = await client.post("/tickets", json=payload)

    ticket = created.json()

    response = await client.get(f"/tickets/{ticket['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == ticket["id"]

@pytest.mark.asyncio
async def test_patch_ticket(client):

    payload = {
        "title": "Patch me",
        "status": "open",
        "priority": "low",
        "description": "",
        "assignee": None,
    }

    created = await client.post("/tickets", json=payload)

    ticket = created.json()

    response = await client.patch(
        f"/tickets/{ticket['id']}",
        json={
            "status": "closed"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "closed"