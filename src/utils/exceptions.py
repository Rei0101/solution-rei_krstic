from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class TicketHubException(Exception):
    """Base application exception from which all others inherit."""

    pass


class ExternalAPIError(TicketHubException):
    """Base exception for external upstream provider failures."""

    pass


class ServiceUnavailableError(ExternalAPIError):
    """Raised when the third-party client times out or goes offline."""

    pass


class TicketNotFoundError(TicketHubException):
    """
    Raised when a requested resource ID is missing from the database
    (HTTP 404).
    """

    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id
        self.message = f"Ticket with ID {ticket_id} does not exist."
        super().__init__(self.message)


class TicketAlreadyExistsError(TicketHubException):
    """
    Raised when creating a resource conflicts with an existing ID
    (HTTP 409).
    """

    def __init__(self, ticket_id: int):
        self.ticket_id = ticket_id
        self.message = (
            f"Conflict: A ticket with ID {ticket_id} already exists."
        )
        super().__init__(self.message)


class InvalidTicketOperationError(TicketHubException):
    """
    Raised when an operation violates a core business validation rule
    (HTTP 400).
    """

    pass


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
