"""Exceptions raised by vigilant-robot."""


class ScratchAPIError(Exception):
    """Base exception for client and API errors."""


class ScratchHTTPError(ScratchAPIError):
    """Raised when the API returns an unsuccessful HTTP response."""

    def __init__(self, status_code: int, message: str, url: str) -> None:
        self.status_code = status_code
        self.url = url
        super().__init__(f"{status_code} response from {url}: {message}")
