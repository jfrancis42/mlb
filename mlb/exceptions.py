class MLBError(Exception):
    """Base exception for all MLB SDK errors."""


class MLBHTTPError(MLBError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class MLBNotFoundError(MLBHTTPError):
    pass


class MLBRateLimitError(MLBHTTPError):
    pass


class MLBServerError(MLBHTTPError):
    pass
