# Tests + Reliability

This project includes a baseline test suite to protect the current AI orchestration backend from silent breakage during future changes.

## Purpose

The goal of this test suite is to verify confidence and correctness in the current backend, not to add new features.

It protects the following critical surfaces:

- API endpoint behavior
- request validation
- request-to-contract conversion
- supervisor execution flow
- contract structure stability
- structured error mapping
- response formatting
- basic multi-layer orchestration wiring

## Test structure

```text
tests/
├── api/
│   └── test_query_endpoint.py
├── contracts/
│   └── test_contracts.py
├── supervisor/
│   └── test_main.py
├── reliability/
│   └── test_error_mapping.py
├── integration/
│   └── test_orchestration_flow.py

```

## Run
python -m pytest tests -q

## to run single test

```
python -m pytest tests/api/test_query_endpoint.py -q
python -m pytest tests/contracts/test_contracts.py -q
python -m pytest tests/supervisor/test_main.py -q
python -m pytest tests/reliability/test_error_mapping.py -q
python -m pytest tests/integration/test_orchestration_flow.py -q
```