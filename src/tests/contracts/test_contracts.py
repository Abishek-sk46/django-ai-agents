from ai.core.contracts import (
    AgentResultContract,
    ErrorContract,
    RequestContract,
    SupervisorResultContract,
    ToolResultContract,
)


def test_request_contract_creation():
    contract = RequestContract(
        user_id=1,
        message="find me action movies",
        context={"source": "api"},
        constraints={"limit": 5},
    )

    assert contract.user_id == 1
    assert contract.message == "find me action movies"
    assert contract.context == {"source": "api"}
    assert contract.constraints == {"limit": 5}


def test_error_contract_creation():
    contract = ErrorContract(
        code="INTERNAL_ERROR",
        message="Something went wrong",
        details={"reason": "test"},
    )

    assert contract.code == "INTERNAL_ERROR"
    assert contract.message == "Something went wrong"
    assert contract.details == {"reason": "test"}


def test_tool_result_contract_success_creation():
    contract = ToolResultContract(
        status="success",
        data={"documents": ["doc1", "doc2"]},
        error=None,
        meta={"tool_name": "document_search"},
    )

    assert contract.status == "success"
    assert contract.data == {"documents": ["doc1", "doc2"]}
    assert contract.error is None
    assert contract.meta == {"tool_name": "document_search"}


def test_tool_result_contract_failure_creation():
    error = ErrorContract(
        code="TOOL_ERROR",
        message="Tool failed",
        details={},
    )

    contract = ToolResultContract(
        status="failure",
        data=None,
        error=error,
        meta={"tool_name": "document_search"},
    )

    assert contract.status == "failure"
    assert contract.data is None
    assert contract.error.code == "TOOL_ERROR"
    assert contract.error.message == "Tool failed"
    assert contract.meta == {"tool_name": "document_search"}


def test_agent_result_contract_success_creation():
    contract = AgentResultContract(
        status="success",
        agent="movie_agent",
        output={"message": "Here are your movies"},
        error=None,
        meta={"agent_name": "movie_agent"},
    )

    assert contract.status == "success"
    assert contract.agent == "movie_agent"
    assert contract.output == {"message": "Here are your movies"}
    assert contract.error is None
    assert contract.meta == {"agent_name": "movie_agent"}


def test_agent_result_contract_failure_creation():
    error = ErrorContract(
        code="AGENT_ERROR",
        message="Agent failed",
        details={},
    )

    contract = AgentResultContract(
        status="failure",
        agent="movie_agent",
        output=None,
        error=error,
        meta={"agent_name": "movie_agent"},
    )

    assert contract.status == "failure"
    assert contract.agent == "movie_agent"
    assert contract.output is None
    assert contract.error.code == "AGENT_ERROR"
    assert contract.error.message == "Agent failed"
    assert contract.meta == {"agent_name": "movie_agent"}


def test_supervisor_result_contract_success_creation():
    contract = SupervisorResultContract(
        status="success",
        selected_agent="movie_agent",
        result={"message": "Here are some action movies for you."},
        error=None,
        meta={},
    )

    assert contract.status == "success"
    assert contract.selected_agent == "movie_agent"
    assert contract.result == {"message": "Here are some action movies for you."}
    assert contract.error is None
    assert contract.meta == {}


def test_supervisor_result_contract_failure_creation():
    error = ErrorContract(
        code="INTERNAL_ERROR",
        message="Supervisor failed",
        details={},
    )

    contract = SupervisorResultContract(
        status="failure",
        selected_agent=None,
        result=None,
        error=error,
        meta={},
    )

    assert contract.status == "failure"
    assert contract.selected_agent is None
    assert contract.result is None
    assert contract.error.code == "INTERNAL_ERROR"
    assert contract.error.message == "Supervisor failed"
    assert contract.meta == {}