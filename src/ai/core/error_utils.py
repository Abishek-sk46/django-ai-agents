# src/ai/core/error_utils.py

from ai.core.contracts import ErrorContract
from ai.core.error_codes import INTERNAL_ERROR
from ai.core.exceptions import AppError


def map_exception_to_error_contract(exc: Exception) -> ErrorContract:
    if isinstance(exc, AppError):
        return ErrorContract(
            code=exc.code,
            message=exc.message,
            details=exc.details,
        )

    return ErrorContract(
        code=INTERNAL_ERROR,
        message="An unexpected internal error occurred",
        details={"reason": str(exc)},
    )