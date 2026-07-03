from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ticket import Ticket
from src.services.dummyjson import fetch_todos, fetch_users


def transform_todo(todo: dict, users: dict[int, str]) -> dict:
    return {
        "id": todo["id"],
        "title": todo["todo"],
        "status": "closed" if todo["completed"] else "open",
        "priority": ["low", "medium", "high"][todo["id"] % 3],
        "assignee": users.get(todo["userId"]),
        "raw_source": todo,
    }


async def sync_tickets(db: AsyncSession) -> None:
    await db.execute(delete(Ticket))

    todos_data = await fetch_todos()
    users_data = await fetch_users()

    users = {user["id"]: user["username"] for user in users_data["users"]}
    todos = todos_data["todos"]

    tickets_data = [transform_todo(todo, users) for todo in todos]

    tickets = [
        Ticket(
            id=t["id"],
            title=t["title"],
            status=t["status"],
            priority=t["priority"],
            assignee=t["assignee"],
            raw_source=t["raw_source"],
        )
        for t in tickets_data
    ]

    db.add_all(tickets)
    await db.commit()

    await db.flush()
