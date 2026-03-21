from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ErrorContract:
    code: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RequestContract:
    user_id: Optional[int] = None
    message: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResultContract:
    status: str
    data: Optional[Any] = None
    error: Optional[ErrorContract] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResultContract:
    status: str
    agent: str
    output: Optional[Any] = None
    error: Optional[ErrorContract] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SupervisorResultContract:
    status: str
    selected_agent: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[ErrorContract] = None
    meta: Dict[str, Any] = field(default_factory=dict)