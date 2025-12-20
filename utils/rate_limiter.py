
"""
Rate Limiter
Circuit breaker pattern for graceful degradation
"""

import time
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiting with circuit breaker"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = []
        self.is_open = False
        self.failure_count = 0
    
    def is_allowed(self) -> bool:
        """Check if request is allowed"""
        now = time.time()
        self.requests = [req for req in self.requests if now - req < self.window]
        
        if self.is_open:
            logger.warning("Circuit breaker OPEN")
            return False
        
        if len(self.requests) >= self.max_requests:
            self.failure_count += 1
            logger.warning("Rate limit exceeded")
            return False
        
        self.requests.append(now)
        return True
    
    def get_status(self) -> Dict:
        """Get limiter status"""
        return {
            "is_open": self.is_open,
            "requests_in_window": len(self.requests),
            "max_requests": self.max_requests,
            "failure_count": self.failure_count
        }
