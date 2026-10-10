"""
Thread-safe rate limiter for upstream API querying.
"""

import time
import threading

class RateLimiter:
    """
    Ensures minimum time interval between consecutive external HTTP requests.
    """
    def __init__(self, requests_per_minute: int = 30):
        if requests_per_minute <= 0:
            raise ValueError("requests_per_minute must be positive")
        self.interval = 60.0 / requests_per_minute
        self.lock = threading.Lock()
        self.last_call_time = 0.0

    def wait(self):
        """Blocks execution until the required interval has passed."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call_time
            if elapsed < self.interval:
                sleep_time = self.interval - elapsed
                time.sleep(sleep_time)
            self.last_call_time = time.time()
