# AI Agent System - Project Structure

## Folder Structure

```
AI-AGENT/
│
├── src/                          # Main Django application
│   ├── neurocore/               # Project settings and configuration
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── ai/                       # AI agents and core AI logic
│   │   ├── agents/              # Individual AI agents
│   │   │   ├── document_agent.py
│   │   │   ├── github_agent.py
│   │   │   └── movie_agent.py
│   │   │
│   │   ├── tools/               # AI tools and integrations
│   │   │   ├── documents.py
│   │   │   ├── github_tool.py
│   │   │   ├── movie_discovery.py
│   │   │   └── clients/         # External API clients
│   │   │       └── github_client.py
│   │   │
│   │   ├── supervisor/          # Multi-agent supervision
│   │   │   └── main.py
│   │   │
│   │   ├── core/                # Core AI utilities
│   │   │   ├── contracts.py
│   │   │   ├── error_codes.py
│   │   │   ├── error_utils.py
│   │   │   ├── exceptions.py
│   │   │   ├── llm.py
│   │   │   ├── logger.py
│   │   │   └── tracing.py
│   │   │
│   │   ├── api/                 # API endpoints and serializers
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   │
│   │   ├── models.py            # AI domain models
│   │   ├── app.py               # Django app configuration
│   │   └── migrations/          # Database migrations
│   │
│   ├── documents/               # Document management app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── mypermit/                # Permission management client
│   │   └── client.py
│   │
│   ├── tmdb/                    # TMDB movie API client
│   │   └── client.py
│   │
│   ├── tests/                   # Test suite
│   │   ├── test_smoke.py
│   │   ├── api/                 # API tests
│   │   │   └── test_query_endpoint.py
│   │   ├── contracts/           # Contract tests
│   │   │   └── test_contracts.py
│   │   ├── integration/         # Integration tests
│   │   │   ├── test_github_integration.py
│   │   │   └── test_orchestration_flow.py
│   │   ├── reliability/         # Error handling tests
│   │   │   └── test_error_mapping.py
│   │   └── supervisor/          # Supervisor tests
│   │       └── test_main.py
│   │
│   ├── manage.py                # Django management script
│   ├── db.sqlite3               # SQLite database
│   ├── pytest.ini               # Pytest configuration
│   └── TESTING.md               # Testing documentation
│
├── notebook/                    # Jupyter notebooks (examples and testing)
│   ├── 1-hello.ipynb
│   ├── 2-langgraph-django-tools.ipynb
│   ├── 3-verify-ll-django.ipynb
│   ├── 4-hello-world-ai-agent.ipynb
│   ├── 5-agent-crud.ipynb
│   ├── 6-tmdb-api-client.ipynb
│   ├── 7-movie-discovery-ai-agent.ipynb
│   ├── 8-multi-agent-supervisor.ipynb
│   ├── 9-rolesandpermission.ipynb
│   ├── 10-test.ipynb
│   ├── 11-test_dock.ipynb
│   └── setup.py
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # License information
├── test_concurrency.py          # Concurrency tests
│
└── z/                           # Documentation/notes (misc)
    └── R.md
```

## Directory Descriptions

### `/src/` - Main Application

Contains the Django project and all application code.

### `/src/ai/` - AI Core System

Hub for all AI-related functionality including agents, tools, supervisor, and core utilities.

### `/src/ai/agents/` - AI Agents

Individual specialized agents for different domains (documents, GitHub, movies).

### `/src/ai/tools/` - Tools & Integrations

Reusable tools used by agents and external API clients for integration.

### `/src/ai/supervisor/` - Agent Orchestration

Manages multi-agent coordination and workflow orchestration.

### `/src/ai/core/` - Core Utilities

Common utilities for LLM, error handling, logging, and tracing.

### `/src/tests/` - Test Suite

Comprehensive tests organized by test type (unit, integration, reliability).

### `/notebook/` - Jupyter Notebooks

Interactive notebooks for development, testing, and demonstrations.

### Root Files

- `requirements.txt` - Python package dependencies
- `LICENSE` - Project license
- `test_concurrency.py` - Concurrency testing utilities
