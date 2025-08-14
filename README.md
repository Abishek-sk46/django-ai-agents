# AI-AGENT

A sophisticated multi-agent AI system built with Django, LangChain, and LangGraph for intelligent document processing, movie discovery, and role-based access control.

## 🎯 Overview

AI-AGENT is a comprehensive platform that combines multiple AI agents orchestrated through a supervisor pattern to handle various tasks including document management, movie discovery, and user permission management. The system leverages advanced language models and graph-based agent coordination for intelligent task routing and execution.

## ✨ Key Features

- **Multi-Agent Architecture**: Supervisor-coordinated agents using LangGraph
- **Document Management**: AI-powered document processing and querying
- **Movie Discovery**: Integration with TMDB API for intelligent movie search
- **Role-Based Access Control**: Fine-grained permissions using Permit.io
- **Interactive Notebooks**: Jupyter-based development and testing environment
- **Django Backend**: Robust web framework with SQLite database

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Supervisor    │───▶│  Document Agent  │    │  Movie Agent    │
│     Agent       │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Permission    │    │    Document      │    │   TMDB API      │
│   Management    │    │   Processing     │    │  Integration    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.12+
- Virtual Environment
- OpenAI API Key
- TMDB API Key
- Permit.io API Key

## 🚀 Installation

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd AI-AGENT
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create your `.env` file based on the provided template:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here
PERMIT_API_KEY=your_permit_api_key_here

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# Permit.io Configuration
PERMIT_PDP_ENDPOINT=https://cloudpdp.api.permit.io
```

### 4. Django Setup

```bash
cd src
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### 5. Start Development Server

```bash
python manage.py runserver
```

## 📁 Project Structure

```
AI-AGENT/
├── src/                          # Main Django application
│   ├── neurocore/               # Django project settings
│   │   ├── settings.py          # Django configuration
│   │   ├── urls.py              # URL routing
│   │   └── wsgi.py              # WSGI configuration
│   ├── ai/                      # AI agents and coordination
│   │   ├── agents.py            # Individual agent definitions
│   │   ├── supervisors.py       # Supervisor agent logic
│   │   ├── llms.py              # Language model configurations
│   │   └── tools/               # Agent tools
│   │       ├── documents.py     # Document processing tools
│   │       └── movie_discovery.py # Movie search tools
│   ├── documents/               # Document management app
│   │   ├── models.py            # Document data models
│   │   ├── views.py             # Document views
│   │   └── admin.py             # Admin interface
│   ├── mypermit/               # Permit.io integration
│   │   └── client.py           # Permission client
│   └── tmdb/                   # TMDB API integration
│       └── client.py           # TMDB API client
├── notebook/                   # Jupyter notebooks
│   ├── 1-hello.ipynb          # Basic setup verification
│   ├── 2-langgraph-django-tools.ipynb # LangGraph integration
│   ├── 3-verify-ll-django.ipynb # Language model verification
│   ├── 4-hello-world-ai-agent.ipynb # First agent implementation
│   ├── 5-agent-crud.ipynb     # Agent CRUD operations
│   ├── 6-tmdb-api-client.ipynb # TMDB API testing
│   ├── 7-movie-discovery-ai-agent.ipynb # Movie agent
│   ├── 8-multi-agent-supervisor.ipynb # Supervisor pattern
│   └── 9-rolesandpermission.ipynb # Permission system
├── requirements.txt            # Python dependencies
└── .env                       # Environment variables
```

## 🤖 Agent System

### Core Components

1. **Supervisor Agent** (`ai/supervisors.py`)
   - Orchestrates multiple specialized agents
   - Routes user requests to appropriate agents
   - Manages conversation context and flow

2. **Document Agent** (`ai/tools/documents.py`)
   - Handles document upload and processing
   - Provides document search and querying capabilities
   - Manages document-related permissions

3. **Movie Discovery Agent** (`ai/tools/movie_discovery.py`)
   - Integrates with TMDB API for movie data
   - Provides intelligent movie search and recommendations
   - Handles movie-related queries and information retrieval

### Agent Tools

- **Document Tools**: File processing, content extraction, semantic search
- **Movie Tools**: TMDB API integration, search, recommendations, detailed movie information

## 🔐 Permission Management

The system uses Permit.io for comprehensive role-based access control:

### Resources
- **Documents**: create, read, update, delete operations
- **Movie Discovery**: search and detail access

### Implementation
- Integrated through `mypermit/client.py`
- Cloud-based policy decision point
- Fine-grained permission checks per operation

## 📊 Development Notebooks

The `notebook/` directory contains progressive development examples:

1. **Setup & Verification** (1-3): Basic system setup and verification
2. **Agent Development** (4-5): Individual agent creation and testing
3. **API Integration** (6-7): External API integration and testing
4. **Multi-Agent System** (8): Supervisor pattern implementation
5. **Permissions** (9): Role-based access control setup

## 🛠️ Technology Stack

- **Backend**: Django 5.0+
- **AI Framework**: LangChain + LangGraph
- **Language Models**: OpenAI GPT models
- **Database**: SQLite (development)
- **Permissions**: Permit.io
- **External APIs**: TMDB (Movie Database)
- **Development**: Jupyter Notebooks
- **Environment**: Python 3.12+

## 🚦 Usage

### Running the Application

```bash
# Start Django development server
cd src
python manage.py runserver
```

### Development with Notebooks

```bash
# Start Jupyter
jupyter notebook

# Navigate to notebook/ directory for examples
```

### Testing Agents

Use the provided notebooks for testing individual components:
- Test basic setup with `1-hello.ipynb`
- Verify agent functionality with `4-hello-world-ai-agent.ipynb`
- Test movie discovery with `7-movie-discovery-ai-agent.ipynb`
- Test multi-agent coordination with `8-multi-agent-supervisor.ipynb`

## 🔧 Configuration

### Django Settings
Main configuration in `src/neurocore/settings.py`

### Agent Configuration
Agent behaviors and prompts defined in `src/ai/agents.py`

### API Integration
- TMDB client: `src/tmdb/client.py`
- Permit client: `src/mypermit/client.py`

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated and dependencies installed
2. **API Key Issues**: Verify all required API keys are set in `.env`
3. **Permission Errors**: Check Permit.io configuration and PDP endpoint
4. **Django Database**: Run migrations if encountering database errors

### Debug Steps

1. Check environment variables are loaded correctly
2. Verify API connectivity in respective notebooks
3. Test individual agents before using supervisor
4. Check Django logs for detailed error information

## 🤝 Contributing

1. Follow the notebook-driven development approach
2. Test individual components before integration
3. Maintain separation between agents and tools
4. Update documentation for new features

## 📄 License

[Specify your license here]

## 🆘 Support

For issues and questions:
- Review the progressive notebooks for usage patterns
- Check individual component tests
- Verify environment configuration
- Consult Django and LangChain documentation

---

**Note**: This project demonstrates advanced AI agent coordination patterns and is suitable for educational and development purposes. Ensure proper API key security in production environments.