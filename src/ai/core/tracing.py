# src/ai/core/tracing.py

from dataclasses import dataclass, field
from typing import Any, Dict, List
from uuid import uuid4


def generate_request_id() -> str:
    return str(uuid4())


@dataclass
class TraceStep:
    layer: str
    event: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceContext:
    request_id: str
    steps: List[TraceStep] = field(default_factory=list)

    def add_step(self, layer: str, event: str, **details):
        self.steps.append(
            TraceStep(
                layer=layer,
                event=event,
                details=details,
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "steps": [
                {
                    "layer": step.layer,
                    "event": step.event,
                    "details": step.details,
                }
                for step in self.steps
            ],
        }