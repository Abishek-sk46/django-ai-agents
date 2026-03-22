from ai.core.error_utils import map_exception_to_error_contract
from ai.core.exceptions import AppError


def test_map_app_error_to_error_contract():
    exc = AppError(
        code="TOOL_ERROR",
        message="Tool failed",
        details={"tool": "document_search"},
    )

    result = map_exception_to_error_contract(exc)

    assert result.code == "TOOL_ERROR"
    assert result.message == "Tool failed"
    assert result.details == {"tool": "document_search"}


def test_map_unknown_exception_to_internal_error_contract():
    exc = Exception("boom")

    result = map_exception_to_error_contract(exc)

    assert result.code == "INTERNAL_ERROR"
    assert result.message == "An unexpected internal error occurred"
    assert result.details == {"reason": "boom"}