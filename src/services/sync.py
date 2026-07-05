import logging

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ticket import Ticket
from src.services.dummyjson import fetch_todos, fetch_users
from src.utils.helpers import transform_todo

logger = logging.getLogger(__name__)


async def sync_tickets(db: AsyncSession) -> None:
    logger.info("Starting ticket synchronization pipeline...")

    try:
        logger.info("Purging old entries from local tickets database table.")
        await db.execute(delete(Ticket))

        logger.info(
            "Fetching fresh payloads from \
                upstream DummyJSON service endpoints..."
        )
        todos_data = await fetch_todos()
        users_data = await fetch_users()

        if "users" not in users_data or "todos" not in todos_data:
            logger.error(
                "Upstream payload structure was missing \
                    expected 'users' or 'todos' arrays."
            )
            raise ValueError("Malformed external API response schema.")

        users = {user["id"]: user["username"] for user in users_data["users"]}
        todos = todos_data["todos"]

        logger.info(
            f"Retrieved {len(todos)} todos \
                and {len(users)} users. Mapping schemas..."
        )
        tickets_data = [transform_todo(todo, users) for todo in todos]

        tickets = [
            Ticket(
                id=t["id"],
                title=t["title"],
                status=t["status"],
                priority=t["priority"],
                description=t["description"],
                assignee=t["assignee"],
                raw_source=t["raw_source"],
            )
            for t in tickets_data
        ]

        db.add_all(tickets)
        await db.commit()
        logger.info(
            f"Successfully committed {len(tickets)} \
                sync records to local database state."
        )

    except Exception as e:
        logger.error(
            f"Database loading transaction \
                aborted due to execution error: {e}",
            exc_info=True,
        )
        await db.rollback()
        raise
