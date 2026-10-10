"""
Abstract Base Adapter for all upstream Ritucast data sources.
"""

import abc
import hashlib
import json
import logging
import os
import time
from typing import Any, Dict, Optional
import requests

from pipelines.common.exceptions import NetworkError, RateLimitError
from pipelines.common.rate_limiter import RateLimiter

logger = logging.getLogger("ritucast.pipeline.adapter")

class BaseAdapter(abc.ABC):
    """
    Standard interface for all dataset ingestion adapters.
    """
    def __init__(
        self,
        source_id: str,
        name: str,
        rate_limiter: Optional[RateLimiter] = None,
        timeout_seconds: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 1.5,
    ):
        self.source_id = source_id
        self.name = name
        self.rate_limiter = rate_limiter
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()

    @abc.abstractmethod
    def fetch_live(self, **kwargs) -> Dict[str, Any]:
        """Fetch live records from external upstream API."""
        pass

    @abc.abstractmethod
    def load_sample(self, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Load synthetic records from local test fixtures."""
        pass

    def _execute_http_get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Executes HTTP GET with rate limiting, timeouts, and exponential backoff retry.
        """
        retries = 0
        last_exception = None

        while retries <= self.max_retries:
            if self.rate_limiter:
                self.rate_limiter.wait()

            try:
                logger.debug(f"[{self.source_id}] Querying GET {url} with params {params}")
                resp = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout_seconds,
                )

                if resp.status_code == 429:
                    raise RateLimitError(f"HTTP 429 Too Many Requests from {url}")

                if resp.status_code >= 500:
                    raise NetworkError(f"Server error HTTP {resp.status_code} from {url}")

                resp.raise_for_status()
                return resp.json()

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, NetworkError, RateLimitError) as err:
                retries += 1
                last_exception = err
                if retries > self.max_retries:
                    logger.error(f"[{self.source_id}] Exceeded max retries ({self.max_retries}) for {url}: {err}")
                    raise NetworkError(f"Failed after {self.max_retries} retries: {err}") from err

                delay = self.backoff_factor ** retries
                logger.warning(f"[{self.source_id}] Transient error {err}. Retrying in {delay:.1f}s (attempt {retries}/{self.max_retries})")
                time.sleep(delay)

            except requests.exceptions.RequestException as err:
                logger.error(f"[{self.source_id}] Non-recoverable client error for {url}: {err}")
                raise NetworkError(f"Non-recoverable HTTP error: {err}") from err

        raise NetworkError(f"Request failed: {last_exception}")

    @staticmethod
    def compute_sha256(data: Any) -> str:
        """Computes SHA-256 hash of arbitrary Python dictionary or string."""
        if isinstance(data, dict) or isinstance(data, list):
            serialized = json.dumps(data, sort_keys=True).encode("utf-8")
        elif isinstance(data, str):
            serialized = data.encode("utf-8")
        elif isinstance(data, bytes):
            serialized = data
        else:
            serialized = str(data).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()
