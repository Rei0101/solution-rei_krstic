import logging
import os

import httpx
from dotenv import load_dotenv

from src.utils.exceptions import ServiceUnavailableError

load_dotenv()

DUMMY_JSON_URL = os.getenv("DUMMY_JSON_URL")


logger = logging.getLogger(__name__)


async def fetch_data(endpoint: str):
    url = f"{DUMMY_JSON_URL}/{endpoint}"
    logger.info(f"Sending GET request to external API endpoint: {url}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()

            logger.info(
                f"Successfully received 200 OK from endpoint: {endpoint}"
            )
            return response.json()

        except httpx.RequestError as e:
            logger.error(
                f"Network transport failure connecting to upstream endpoint\
                      '{endpoint}': {e}",
                exc_info=True,
            )
            raise ServiceUnavailableError("External API unreachable") from e

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Upstream provider returned an error status code:\
                     {e.response.status_code} "
                f"for endpoint: {endpoint}. Details: {e.response.text}"
            )
            raise ServiceUnavailableError(
                f"External API error: {e.response.status_code}"
            ) from e


async def fetch_todos():
    return await fetch_data("todos")


async def fetch_users():
    return await fetch_data("users")
