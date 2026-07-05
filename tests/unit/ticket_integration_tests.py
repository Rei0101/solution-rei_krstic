import pytest
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
