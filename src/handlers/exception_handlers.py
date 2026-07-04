from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.utils.exceptions import (
    InvalidTicketOperationError,
    ServiceUnavailableError,
    TicketAlreadyExistsError,
    TicketNotFoundError,
)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(TicketNotFoundError)
    async def ticket_not_found_handler(
        request: Request, exc: TicketNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": "NOT_FOUND", "message": exc.message},
        )

    @app.exception_handler(TicketAlreadyExistsError)
    async def ticket_already_exists_handler(
        request: Request, exc: TicketAlreadyExistsError
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": "CONFLICT", "message": exc.message},
        )

    @app.exception_handler(InvalidTicketOperationError)
    async def invalid_ticket_operation_handler(
        request: Request, exc: InvalidTicketOperationError
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "BAD_REQUEST", "message": str(exc)},
        )

    @app.exception_handler(ServiceUnavailableError)
    async def service_unavailable_handler(
        request: Request, exc: ServiceUnavailableError
    ):
        return JSONResponse(
            status_code=503,
            content={"detail": "SERVICE_UNAVAILABLE", "message": str(exc)},
        )
