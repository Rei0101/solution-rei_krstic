# TicketHub - solution/rei_krstic

TicketHub is a FastAPI-based backend service that collects, stores, and exposes support tickets from an external source (DummyJSON). The system persists data locally, provides REST endpoints for querying and modifying tickets, and demonstrates async Python, SQLAlchemy, and Alembic migrations. The project includes automated tests, CI pipeline, and Docker support for consistent execution across environments.

---

## Environment Setup

Clone the repository:

```
git clone <repo-url>
cd <repo-name>
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

---

## Configuration Variables

Create a `.env` file based on `.env.example`:

```
DATABASE_URL=sqlite+aiosqlite:///./tickets.db
TEST_DATABASE_URL=sqlite+aiosqlite:///./testdbname.db
DUMMY_JSON_URL=https://dummyjson.com
```

---

## Running the Application

Start the API locally:

```
uvicorn src.main:app --reload
```

API documentation:

```
http://localhost:8000/docs
```

---

## Running Tests

Run unit and integration tests with coverage:

```
pytest --cov=src --cov-report=term-missing
```

---

## Makefile Commands

The project includes a Makefile for common tasks:

```makefile
make install        # install dependencies
make run            # start application
make test           # run tests with coverage
make lint           # run ruff linting
make format         #format code
make docker-build   # build docker image
```

---

## Docker Setup

Build and run the application:

```
docker-compose up --build
```

After starting the containers, run database migrations inside the API container:

```
docker-compose run api alembic upgrade head
```

Stop containers:

```
docker-compose down
```

API available at:

```
http://localhost:8000/docs
```

---

## Database Migrations (Alembic)

Run migrations:

```
alembic upgrade head
```

Create new migration:

```
alembic revision --autogenerate -m "message"
```

---

## CI Pipeline

GitHub Actions runs:

* linting (ruff)
* tests (pytest)
* coverage reporting

---

## API Endpoints

Tickets:

* GET `/tickets`
* GET `/tickets/{id}`
* POST `/tickets`
* PATCH `/tickets/{id}`
* GET `/tickets/search?q=`
* GET `/tickets/stats`

---

## External Data Source

Data is synchronized from:

* [https://dummyjson.com/todos](https://dummyjson.com/todos)
* [https://dummyjson.com/users](https://dummyjson.com/users)

---

## Notes

* Async FastAPI application
* SQLAlchemy async ORM
* External API integration via httpx
* Structured logging and error handling
* Dockerized for reproducible environments

---
