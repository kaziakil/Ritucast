"""
Unit tests for RateLimiter token bucket behavior.
"""

import time
from pipelines.common.rate_limiter import RateLimiter

def test_rate_limiter_interval():
    # 600 requests per minute -> 0.1s interval
    limiter = RateLimiter(requests_per_minute=600)
    t0 = time.time()
    limiter.wait()
    limiter.wait()
    t1 = time.time()
    elapsed = t1 - t0
    assert elapsed >= 0.08  # Tolerant timing check
