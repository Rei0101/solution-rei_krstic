class ExternalAPIError(Exception):
    pass


class ServiceUnavailableError(ExternalAPIError):
    pass
