from unittest.mock import Mock, patch

from ai.core.contracts import ErrorContract, RequestContract
from ai.supervisor.main import (
    _extract_final_message,
    _extract_selected_agent,
    run_supervisor,
)


def test_extract_final_message_from_dict_message():
    response = {
        "messages": [
            {"content": "first"},
            {"content": "final answer"},
        ]
    }

    result = _extract_final_message(response)

    assert result == "final answer"


def test_extract_final_message_from_non_dict_response():
    response = "plain text response"

    result = _extract_final_message(response)

    assert result == "plain text response"


def test_extract_selected_agent_from_top_level_field():
    response = {
        "selected_agent": "movie_agent",
        "messages": [],
    }

    result = _extract_selected_agent(response)

    assert result == "movie_agent"


def test_extract_selected_agent_from_messages():
    response = {
        "messages": [
            {"name": "document_agent", "content": "doc response"},
            {"name": "movie_agent", "content": "movie response"},
        ]
    }

    result = _extract_selected_agent(response)

    assert result == "movie_agent"


def test_run_supervisor_success():
    request = RequestContract(
        user_id=1,
        message="find me action movies",
        context={},
        constraints={},
    )

    mock_supervisor = Mock()
    mock_supervisor.invoke.return_value = {
        "messages": [
            {"name": "movie_agent", "content": "Here are some action movies for you."}
        ]
    }

    with patch("ai.supervisor.main.get_supervisor", return_value=mock_supervisor):
        result = run_supervisor(request, request_id="req-123", trace=None)

    assert result.status == "success"
    assert result.selected_agent == "movie_agent"
    assert result.result == {
        "message": "Here are some action movies for you."
    }
    assert result.error is None
    assert result.meta == {}

    mock_supervisor.invoke.assert_called_once_with(
        {"messages": [("user", "find me action movies")]},
        config={
            "configurable": {
                "user_id": 1,
                "request_id": "req-123",
            }
        },
    )


def test_run_supervisor_failure_when_invoke_raises_exception():
    request = RequestContract(
        user_id=1,
        message="find me action movies",
        context={},
        constraints={},
    )

    mock_supervisor = Mock()
    mock_supervisor.invoke.side_effect = Exception("boom")

    mapped_error = ErrorContract(
        code="INTERNAL_ERROR",
        message="Something went wrong",
        details={},
    )

    with patch("ai.supervisor.main.get_supervisor", return_value=mock_supervisor):
        with patch("ai.supervisor.main.map_exception_to_error_contract", return_value=mapped_error):
            result = run_supervisor(request, request_id="req-123", trace=None)

    assert result.status == "failure"
    assert result.selected_agent is None
    assert result.result is None
    assert result.error.code == "INTERNAL_ERROR"
    assert result.error.message == "Something went wrong"
    assert result.meta == {}