def map_priority(ticket_id: int) -> str:
    match ticket_id % 3:
        case 0:
            return "low"
        case 1:
            return "medium"
        case _:
            return "high"


def transform_todo(todo: dict, users: dict[int, str]) -> dict:
    return {
        "id": todo["id"],
        "title": todo["todo"],
        "status": "closed" if todo["completed"] else "open",
        "priority": map_priority(todo["id"]),
        "description": todo.get("description", ""),
        "assignee": users.get(todo["userId"]),
        "raw_source": todo,
    }
