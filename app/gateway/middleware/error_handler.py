"""
Error Handling Middleware
File: app/gateway/middleware/error_handler.py
Created: 2025-07-17
Purpose: Global error handling for consistent error responses across API
"""

import logging
from typing import Any, Dict, Optional, Awaitable, Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse

from ...shared_kernel.exceptions import TechCoachException

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """Middleware for handling and formatting API errors."""
    
    def __init__(self):
        self.logger = logging.getLogger("techcoach.error")
    
    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Handle errors for all HTTP requests.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain
        
        Returns:
            HTTP response or error response
        """
        try:
            response = await call_next(request)
            return response
            
        except TechCoachException as e:
            # Handle custom application exceptions
            error_response = {
                "error": {
                    "type": type(e).__name__,
                    "message": str(e),
                    "details": e.details
                },
                "request_id": str(request.url.path)
            }
            
            self.logger.warning(
                f"Application error: {type(e).__name__}: {str(e)}",
                extra={"request_path": str(request.url.path)}
            )
            
            return JSONResponse(
                status_code=self._get_status_code(e),
                content=error_response
            )
            
        except Exception as e:
            # Handle unexpected exceptions
            error_response = {
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "details": {"request_path": str(request.url.path)}
                }
            }
            
            self.logger.error(
                f"Unexpected error: {type(e).__name__}: {str(e)}",
                extra={"request_path": str(request.url.path)},
                exc_info=True
            )
            
            return JSONResponse(
                status_code=500,
                content=error_response
            )
    
    def _get_status_code(self, exception: TechCoachException) -> int:
        """Get HTTP status code for TechCoachException."""
        from ...shared_kernel.exceptions import (
            ValidationException,
            NotFoundException,
            AuthenticationException,
            RateLimitException
        )
        
        if isinstance(exception, ValidationException):
            return 400
        elif isinstance(exception, NotFoundException):
            return 404
        elif isinstance(exception, AuthenticationException):
            return 401
        elif isinstance(exception, RateLimitException):
            return 429
        else:
            return 500