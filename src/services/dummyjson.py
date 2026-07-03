import os

import httpx
from dotenv import load_dotenv

load_dotenv()
DUMMY_JSON_URL = os.getenv("DUMMY_JSON_URL")


async def fetch_todos() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DUMMY_JSON_URL}/todos")
        response.raise_for_status()
        return response.json()


async def fetch_users() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DUMMY_JSON_URL}/users")
        response.raise_for_status()
        return response.json()
