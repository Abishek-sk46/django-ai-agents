# AI Agent System

Multi-agent AI system built with Django and LangChain for document processing and movie discovery.

## Features

- Document management with AI processing
- Movie discovery using TMDB API
- Role-based permissions
- Multi-agent coordination

## Prerequisites

- Python 3.12+
- OpenAI API Key
- TMDB API Key
- Permit.io API Key

## Installation

1. Clone repository and setup environment:
```bash
git clone <repository-url>
cd AI-AGENT
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. Create .env file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here
PERMIT_API_KEY=your_permit_api_key_here
DEBUG=True
SECRET_KEY=your-secret-key-here
```

3. Setup Django:
```bash
cd src
python manage.py migrate
python manage.py runserver
```

## Project Structure

```
src/                    # Django application
├── neurocore/         # Project settings
├── ai/                # AI agents and tools
├── documents/         # Document management
├── mypermit/          # Permission management
└── tmdb/              # Movie API client

notebook/              # Jupyter notebooks for testing
```

## Usage

Start the Django server:
```bash
cd src
python manage.py runserver
```

For development and testing, use the Jupyter notebooks in the `notebook/` directory.