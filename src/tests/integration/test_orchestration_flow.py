from unittest.mock import patch

from rest_framework.test import APIClient

from ai.core.contracts import SupervisorResultContract, ErrorContract


def test_api_to_supervisor_success_flow():
    client = APIClient()

    payload = {
        "message": "find me action movies",
        "user_id": 1,
        "context": {},
        "constraints": {},
    }

    mocked_result = SupervisorResultContract(
        status="success",
        selected_agent="movie_agent",
        result={
            "message": "Here are some action movies for you."
        },
        error=None,
        meta={},
    )

    with patch("ai.api.views.run_supervisor", return_value=mocked_result) as mock_run_supervisor:
        response = client.post("/api/agent/query", payload, format="json")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["selected_agent"] == "movie_agent"
    assert data["result"] == {
        "message": "Here are some action movies for you."
    }
    assert data["error"] is None
    assert "meta" in data
    assert "request_id" in data["meta"]
    assert "steps" in data["meta"]

    mock_run_supervisor.assert_called_once()


def test_api_to_supervisor_failure_flow():
    client = APIClient()

    payload = {
        "message": "find me action movies",
        "user_id": 1,
        "context": {},
        "constraints": {},
    }

    mocked_result = SupervisorResultContract(
        status="failure",
        selected_agent=None,
        result=None,
        error=ErrorContract(
            code="INTERNAL_ERROR",
            message="Something went wrong",
            details={},
        ),
        meta={},
    )

    with patch("ai.api.views.run_supervisor", return_value=mocked_result) as mock_run_supervisor:
        response = client.post("/api/agent/query", payload, format="json")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "failure"
    assert data["selected_agent"] is None
    assert data["result"] is None
    assert data["error"]["code"] == "INTERNAL_ERROR"
    assert data["error"]["message"] == "Something went wrong"
    assert "meta" in data
    assert "request_id" in data["meta"]
    assert "steps" in data["meta"]

    mock_run_supervisor.assert_called_once()