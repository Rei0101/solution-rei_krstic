import os

import httpx
from dotenv import load_dotenv

from src.exceptions import ServiceUnavailableError

load_dotenv()

DUMMY_JSON_URL = os.getenv("DUMMY_JSON_URL")


async def fetch_data(endpoint: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{DUMMY_JSON_URL}/{endpoint}")
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as e:
            raise ServiceUnavailableError("External API unreachable") from e

        except httpx.HTTPStatusError as e:
            raise ServiceUnavailableError(
                f"External API error: {e.response.status_code}"
            ) from e


async def fetch_todos():
    return await fetch_data("todos")


async def fetch_users():
    return await fetch_data("users")
