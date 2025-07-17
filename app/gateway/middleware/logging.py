"""
Request Logging Middleware
File: app/gateway/middleware/logging.py
Created: 2025-07-17
Purpose: HTTP request/response logging middleware using starlette
"""

import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and their responses."""
    
    async def dispatch(self, request, call_next):
        """Process and log each HTTP request."""
        start_time = time.time()
        
        logger.info(
            f"Incoming request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            logger.info(
                f"Response: {response.status_code} "
                f"duration={duration:.3f}s "
                f"URL={request.url.path}"
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Error processing request: {request.method} {request.url.path} "
                f"duration={duration:.3f}s error={str(e)}"
            )
            raise