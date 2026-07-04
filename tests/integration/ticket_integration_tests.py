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
        json={"status": "closed"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "closed"


@pytest.mark.asyncio
async def test_patch_already_closed_ticket_throws_400(client):
    created = await client.post(
        "/tickets",
        json={
            "title": "Immutable ticket",
            "status": "open",
            "priority": "low",
            "description": "",
        },
    )

    ticket_id = created.json()["id"]

    await client.patch(f"/tickets/{ticket_id}", json={"status": "closed"})

    response = await client.patch(
        f"/tickets/{ticket_id}", json={"status": "closed"}
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"]["code"] == "BAD_REQUEST"
    assert "already closed and finalized" in data["detail"]["message"]


@pytest.mark.asyncio
async def test_ticket_not_found(client):
    response = await client.get("/tickets/999999")
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "NOT_FOUND"
    assert "does not exist" in data["message"]


@pytest.mark.asyncio
async def test_filter_status(client):

    response = await client.get("/tickets?status=open")

    assert response.status_code == 200

    data = response.json()

    for ticket in data["items"]:
        assert ticket["status"] == "open"


@pytest.mark.asyncio
async def test_search(client):

    response = await client.get("/tickets/search?q=Learn")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data


@pytest.mark.asyncio
async def test_stats(client):

    response = await client.get("/tickets/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "status" in data
    assert "priority" in data


@pytest.mark.asyncio
async def test_ticket_lifecycle(client):

    payload = {
        "title": "DB test ticket",
        "status": "open",
        "priority": "high",
        "description": "integration test",
        "assignee": "john",
    }

    create_res = await client.post("/tickets", json=payload)
    assert create_res.status_code == 201

    ticket = create_res.json()
    ticket_id = ticket["id"]

    get_res = await client.get(f"/tickets/{ticket_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "DB test ticket"

    patch_res = await client.patch(
        f"/tickets/{ticket_id}", json={"status": "closed"}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "closed"

    get_again = await client.get(f"/tickets/{ticket_id}")
    assert get_again.json()["status"] == "closed"
