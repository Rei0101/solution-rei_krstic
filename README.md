# TicketHub - solution/rei_krstic

TicketHub is a FastAPI-based backend service that collects, stores, and exposes support tickets from an external source (DummyJSON). The system persists data locally, provides REST endpoints for querying and modifying tickets, and demonstrates async Python, SQLAlchemy, and Alembic migrations. The project includes automated tests, CI pipeline, and Docker support for consistent execution across environments.

## Requirements

* Python 3.11
* Docker & Docker Compose (optional)

## Local or Docker Setup

### Local Environment Setup

Clone the repository:

```
git clone <repo-url>
cd <repo-name>
```

Create a `.env` file based on `.env.example`:

```
DATABASE_URL=sqlite+aiosqlite:///./tickets.db
TEST_DATABASE_URL=sqlite+aiosqlite:///./testdb.db
DUMMY_JSON_URL=https://dummyjson.com
```

Create virtual environment (optional):

```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

Install dependencies:

```
pip install -r requirements.txt
```

Run Alembic migrations locally:

```
alembic upgrade head
```

Start the API locally:

```
uvicorn src.main:app --reload
```

Run unit and integration tests with coverage:

```
pytest --cov=src --cov-report=term-missing
```

API will be available at:

```
http://localhost:8000/docs
```

### Docker Setup

Build and run the application:

```
docker-compose up --build
```

After starting the containers, run database migrations inside the API container:

```
docker-compose run api alembic upgrade head
```

API will be available at:

```
http://localhost:8000/docs
```

## Makefile Commands

Common development tasks can also be executed using the provided Makefile:

```makefile
make install        # install dependencies
make run            # start application
make test           # run tests with coverage
make lint           # run ruff linting
make format         # format code
make docker-build   # build docker image
```

## CI Pipeline

GitHub Actions runs:

* installing requirements
* linting and checking formatting (ruff)
* tests and coverage reporting (pytest)

The workflow is located at: `.github/workflows/ci.yml`

## API Ticket Endpoints

* GET `/tickets`
* GET `/tickets/{id}`
* POST `/tickets`
* PATCH `/tickets/{id}`
* GET `/tickets/search?q=`
* GET `/tickets/stats`

## External Data Source

Data is synchronized from:

* [https://dummyjson.com/todos](https://dummyjson.com/todos)
* [https://dummyjson.com/users](https://dummyjson.com/users)

## AI Usage Disclosure

AI tools (more specifically, ChatGPT, Gemini, and Windsurf/Codeium in case better code context was needed for a prompt) were used during development of this project to assist with tasks such as (but not limited to) generating boilerplate and example code, understanding syntax and foreign concepts quickly (reminiscent of a cheat sheet and a substitute for long documentation to compensate for the relatively short deadline of ~1 week), brainstorming decisions, debugging and resolving issues, as well as writing this README.md.

For example, as I have never used the tech stack used for this particular project before, but am nonetheless familiar with concepts from another stack, the following "system" prompt was given to the above mentioned AI tools:

```
You are a senior Python backend developer acting as a mentor.

I have experience with the MERN/PERN stack and a solid understanding of backend concepts such as REST APIs, HTTP, CRUD, SQL, asynchronous programming, and general software architecture. I am comfortable with Python syntax but new to FastAPI and its ecosystem.

When helping me:
- Explain FastAPI, SQLAlchemy, Pydantic, Alembic, httpx, and other Python-specific concepts.
- Prefer clean, maintainable, and idiomatic solutions over quick fixes.
- Explain the reasoning behind design decisions and discuss trade-offs when relevant.
- Compare concepts to Express/PERN when it helps bridge the gap.
- Generate only the code needed for the current task rather than the entire application.
- Point out potential issues, anti-patterns, or better approaches when appropriate.
- Assume I want to understand the implementation rather than simply complete the task.
```

All final code decisions, architecture choices, and implementation details were reviewed and approved/adjusted manually by the author, who takes full responsibility for them.
