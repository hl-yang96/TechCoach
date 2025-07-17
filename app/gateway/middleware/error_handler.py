"""
Error Handling Middleware
File: app/gateway/middleware/error_handler.py
Created: 2025-07-17
Purpose: Global error handling for consistent API responses
"""

import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling and formatting API errors."""
    
    async def dispatch(self, request, call_next):
        """Handle errors for all HTTP requests."""
        try:
            return await call_next(request)
            
        except Exception as e:
            error_response = {
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "details": {"type": type(e).__name__, "message": str(e)}
                }
            }
            
            logger.error(
                f"Unhandled error: {type(e).__name__}: {str(e)}",
                extra={"request_path": str(request.url.path)}
            )
            
            return JSONResponse(status_code=500, content=error_response)