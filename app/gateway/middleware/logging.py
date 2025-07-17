"""
Request Logging Middleware
File: app/gateway/middleware/logging.py
Created: 2025-07-17
Purpose: Request/response logging for monitoring and debugging
"""

import time
import logging
from typing import Awaitable, Callable
from fastapi import Request, Response

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """Middleware for logging HTTP requests and their responses."""
    
    def __init__(self):
        self.logger = logging.getLogger("techcoach.request")
    
    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process and log each HTTP request.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain
        
        Returns:
            HTTP response
        """
        start_time = time.time()
        
        # Log incoming request
        self.logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            
            # Calculate processing time
            duration = time.time() - start_time
            
            # Log response
            self.logger.info(
                f"Response: {response.status_code} "
                f"duration={duration:.3f}s "
                f"URL={request.url.path}"
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                f"Error processing request: {request.method} {request.url.path} "
                f"duration={duration:.3f}s error={str(e)}"
            )
            raise