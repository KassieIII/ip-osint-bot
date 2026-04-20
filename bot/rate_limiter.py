import time
from collections import defaultdict


class RateLimiter:
    """Simple in-memory per-user rate limiter using sliding window."""

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: dict[int, list[float]] = defaultdict(list)

    def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        timestamps = self._requests[user_id]

        # Remove expired timestamps
        self._requests[user_id] = [
            ts for ts in timestamps if now - ts < self.window
        ]

        if len(self._requests[user_id]) >= self.max_requests:
            return False

        self._requests[user_id].append(now)
        return True
