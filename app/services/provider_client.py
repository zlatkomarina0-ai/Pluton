import random
import time
from typing import Any, Dict, Optional, Tuple

import requests

from app.config import settings


class ProviderClient:
    def __init__(
        self,
        timeout_seconds: Optional[int] = None,
        max_retries: Optional[int] = None,
        backoff_base_seconds: Optional[float] = None,
        rate_limit_per_minute: Optional[int] = None,
    ):
        self.timeout_seconds = timeout_seconds or settings.PROVIDER_TIMEOUT_SECONDS
        self.max_retries = max_retries or settings.PROVIDER_MAX_RETRIES
        self.backoff_base_seconds = backoff_base_seconds or settings.PROVIDER_BACKOFF_BASE_SECONDS
        self.rate_limit_per_minute = max(1, rate_limit_per_minute or settings.PROVIDER_RATE_LIMIT_PER_MINUTE)

        self._last_call_ts = 0.0

    def _wait_for_rate_limit(self) -> None:
        period = 60.0 / self.rate_limit_per_minute
        elapsed = time.monotonic() - self._last_call_ts
        if self._last_call_ts and elapsed < period:
            time.sleep(period - elapsed)
        self._last_call_ts = time.monotonic()

    def _sleep_backoff(self, attempt: int) -> None:
        backoff = self.backoff_base_seconds * (2 ** attempt)
        jitter = random.uniform(0, backoff * 0.3)
        time.sleep(backoff + jitter)

    def fetch_json(self, url: str, method: str = "GET", json_body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Tuple[Any, int]:
        effective_headers = {"Accept": "application/json"}
        if headers:
            effective_headers.update(headers)

        for attempt in range(self.max_retries + 1):
            self._wait_for_rate_limit()

            try:
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    json=json_body,
                    headers=effective_headers,
                    timeout=self.timeout_seconds,
                )

                if response.status_code in {429, 500, 502, 503, 504}:
                    if attempt < self.max_retries:
                        self._sleep_backoff(attempt)
                        continue

                response.raise_for_status()
                try:
                    payload = response.json()
                except ValueError:
                    payload = response.text
                return payload, response.status_code

            except requests.Timeout:
                if attempt < self.max_retries:
                    self._sleep_backoff(attempt)
                    continue
                raise

            except requests.HTTPError as exc:
                if attempt < self.max_retries and exc.response is not None and exc.response.status_code in {429, 500, 502, 503, 504}:
                    self._sleep_backoff(attempt)
                    continue
                raise

            except requests.RequestException:
                if attempt < self.max_retries:
                    self._sleep_backoff(attempt)
                    continue
                raise
