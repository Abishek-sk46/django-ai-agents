# src/ai/core/exceptions.py

from typing import Any, Dict, Optional

from ai.core.error_codes import (
    AGENT_ERROR,
    INTERNAL_ERROR,
    ROUTING_ERROR,
    TOOL_ERROR,
    VALIDATION_ERROR,
)


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


class ValidationAppError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(VALIDATION_ERROR, message, details)


class RoutingAppError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(ROUTING_ERROR, message, details)


class ToolAppError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(TOOL_ERROR, message, details)


class AgentAppError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(AGENT_ERROR, message, details)


class InternalAppError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(INTERNAL_ERROR, message, details)