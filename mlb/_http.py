from __future__ import annotations

import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import MLBHTTPError, MLBNotFoundError, MLBRateLimitError, MLBServerError

BASE_URL = "https://statsapi.mlb.com/api"


def _build_session(timeout: int, max_retries: int) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=max_retries,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.headers.update({"Accept": "application/json"})
    session.timeout = timeout
    return session


class HTTPClient:
    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        rate_limit_delay: float = 0.0,
    ):
        self._session = _build_session(timeout, max_retries)
        self._timeout = timeout
        self._rate_limit_delay = rate_limit_delay
        self._last_request: float = 0.0

    def get(self, path: str, api_version: str = "v1", **params: Any) -> dict:
        if self._rate_limit_delay > 0:
            elapsed = time.monotonic() - self._last_request
            if elapsed < self._rate_limit_delay:
                time.sleep(self._rate_limit_delay - elapsed)

        url = f"{BASE_URL}/{api_version}/{path.lstrip('/')}"
        # Remove None params so they don't appear as "None" strings
        clean_params = {k: v for k, v in params.items() if v is not None}

        self._last_request = time.monotonic()
        resp = self._session.get(url, params=clean_params, timeout=self._timeout)
        return self._raise_for_status(resp)

    @staticmethod
    def _raise_for_status(resp: requests.Response) -> dict:
        if resp.ok:
            return resp.json()
        if resp.status_code == 404:
            raise MLBNotFoundError(404, resp.text[:200])
        if resp.status_code == 429:
            raise MLBRateLimitError(429, "Rate limit exceeded")
        if resp.status_code >= 500:
            raise MLBServerError(resp.status_code, resp.text[:200])
        raise MLBHTTPError(resp.status_code, resp.text[:200])
