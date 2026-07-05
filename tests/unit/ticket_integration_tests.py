from unittest.mock import AsyncMock, patch

import pytest

from src.services.sync import sync_tickets
from src.utils.helpers import map_priority, transform_todo


def test_priority_mapping():
    assert map_priority(1) in ["low", "medium", "high"]


def test_ticket_transform():
    todo = {"id": 1, "todo": "Learn FastAPI", "completed": True, "userId": 2}

    users_mock_dict = {2: "john"}

    result = transform_todo(todo, users_mock_dict)

    assert result["id"] == 1
    assert result["title"] == "Learn FastAPI"
    assert result["status"] == "closed"
    assert result["priority"] == "medium"
    assert result["description"] == ""
    assert result["assignee"] == "john"
    assert result["raw_source"] == todo


@pytest.mark.asyncio
@patch("src.services.sync.fetch_users")
@patch("src.services.sync.fetch_todos")
async def test_sync_tickets(mock_fetch_todos, mock_fetch_users):
    mock_db = AsyncMock()

    mock_fetch_todos.return_value = {
        "todos": [
            {
                "id": 1,
                "todo": "Test",
                "completed": False,
                "userId": 1,
            }
        ]
    }

    mock_fetch_users.return_value = {
        "users": [
            {
                "id": 1,
                "username": "john",
            }
        ]
    }

    await sync_tickets(mock_db)

    mock_db.add_all.assert_called_once()
    mock_db.commit.assert_awaited_once()
