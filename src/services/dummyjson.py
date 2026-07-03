import os

import httpx
from dotenv import load_dotenv

load_dotenv()
DUMMY_JSON_URL = os.getenv("DUMMY_JSON_URL")


async def fetch_data(endpoint: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DUMMY_JSON_URL}/{endpoint}")
        response.raise_for_status()
        data = response.json()
        return data


async def fetch_todos():
    return await fetch_data("todos")


async def fetch_users():
    return await fetch_data("users")