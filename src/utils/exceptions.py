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