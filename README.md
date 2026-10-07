# TaskManagementAPI

A FastAPI task-management API with JWT authentication, SQLAlchemy, and
Alembic migrations. All task operations are scoped to the authenticated user.

## Architecture

```text
app/
├── api/             FastAPI routes
├── schemas/         Pydantic request/response models
├── services/        Business logic and ownership checks
├── repositories/    Database access
├── models/          SQLAlchemy models
├── dependencies.py  Shared FastAPI dependencies
└── security.py      Password hashing and JWT handling
```

Routes validate requests and delegate to services. Services enforce ownership
and use repositories for persistence.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set the environment variables before running migrations:

```bash
export DATABASE_URL="sqlite:///./tasks.db"
export SECRET_KEY="replace-with-a-strong-secret"
```

`SECRET_KEY` should always be changed outside local development.

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API runs at <http://127.0.0.1:8000>. Swagger UI is available at
<http://127.0.0.1:8000/docs>.

## Migrations

Apply migrations:

```bash
alembic upgrade head
```

Create a migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the change"
```

## Authentication

Register or log in:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"strong-password"}'

curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"strong-password"}'
```

Use the returned token for task requests:

```text
Authorization: Bearer <access_token>
```

## API

All task endpoints require authentication.

```bash
# List tasks
curl http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer <access_token>"

# Create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","description":"Build the API","priority":"high"}'

# Get, update, or delete a task
curl http://127.0.0.1:8000/tasks/1 \
  -H "Authorization: Bearer <access_token>"

curl -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","description":"Finish the API","status":"done","priority":"high"}'

curl -X DELETE http://127.0.0.1:8000/tasks/1 \
  -H "Authorization: Bearer <access_token>"
```

Supported statuses are `todo`, `in_progress`, and `done`. Supported
priorities are `low`, `medium`, and `high`.

## Testing

```bash
pytest
```

Tests use an isolated SQLite database and a seeded test user.
