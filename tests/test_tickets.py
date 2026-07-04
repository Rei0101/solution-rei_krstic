import pytest


@pytest.mark.asyncio
async def test_get_tickets(client):
    response = await client.get("/tickets")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)