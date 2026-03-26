# src/ai/core/logger.py

import logging
from typing import Any


logger = logging.getLogger("ai")


def log_event(event: str, layer: str, request_id: str, **kwargs: Any) -> None:
    logger.info(
        {
            "event": event,
            "layer": layer,
            "request_id": request_id,
            **kwargs,
        }
    )