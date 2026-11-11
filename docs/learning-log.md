
# DevOps Learning Log — Containerized Application

This document records the concepts, practical exercises, troubleshooting
experiences, and engineering lessons learned throughout this project.

The objective is not only to complete the project but to understand
the technologies and develop an engineering mindset.

---

## Project Information

- Project: Containerized Application
- Repository: containerized-app
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Cache: Redis
- Containerization: Docker
- Orchestration: Docker Compose

---

# Lesson 00 — Environment Inspection

**Status:** Completed

## 1. Objective

Understand the existing development environment before modifying it.

## 2. Environment

- OS: Ubuntu 24.04.5 LTS
- Architecture: x86_64
- CPU: 2 vCPU
- RAM: 3.8 GiB
- Available disk: approximately 5.1 GB
- Docker Engine: 29.9.3
- Docker Compose: 5.7.0
- Python: 3.12.3
- Git: 2.43.0

## 3. Concepts learned

### Docker Client

The command-line interface used to communicate with Docker Engine.

### Docker Daemon

The background service responsible for managing containers, images,
networks, and volumes.

### Docker Image

A read-only template used to create containers.

### Docker Container

An isolated runtime instance created from an image.

### Docker Compose

A tool for defining and managing multi-container applications.

### Git Remote

A reference to a remote repository, such as GitHub.

## 4. Commands practiced

```bash
pwd
ls -lah
git --version
docker --version
docker compose version
docker info
docker ps -a
docker images
free -h
df -h /
nproc
```

## 5. Observations

- Docker Client communicates successfully with Docker Engine.
- Two hello-world containers exited successfully.
- Git local branch main is synchronized with origin/main.
- The environment has limited disk capacity, so image sizes must be monitored.

## 6. Engineering lessons

- Inspect an environment before modifying it.
- Distinguish the Docker Client from the Docker Daemon.
- Monitor system resources before deploying services.
- Verify Git synchronization before making changes.

---

# Lesson 01 — Three-Tier Architecture

**Status:** In progress

## 1. Objective

Understand the responsibilities and communication mechanisms of
the three application services.

## 2. Architecture

The application consists of three independent services:

1. FastAPI — Backend and business logic.
2. PostgreSQL — Persistent data storage.
3. Redis — In-memory caching.

## 3. Service responsibilities

### FastAPI

- Receives HTTP requests.
- Implements application logic.
- Communicates with PostgreSQL and Redis.
- Returns API responses.

### PostgreSQL

- Stores application data permanently.
- Handles SQL queries.
- Remains the primary source of truth.

### Redis

- Stores temporary cached data.
- Reduces repeated database queries.
- Improves response times.
- Must not replace PostgreSQL as permanent storage.

## 4. Network communication

Planned service endpoints:

| Service | Internal address | Port |
|---|---|---|
| FastAPI | api:8000 | 8000 |
| PostgreSQL | postgres:5432 | 5432 |
| Redis | redis:6379 | 6379 |

These service names will be resolved through Docker Compose DNS.

## 5. Important concepts

- Service isolation
- Network communication
- DNS service discovery
- Cache HIT and Cache MISS
- Persistent storage
- Fault tolerance
- Scalability

## 6. Engineering lessons

- Each service should have one primary responsibility.
- PostgreSQL is the source of truth.
- Redis is an optimization, not a requirement for permanent data storage.
- Application behavior must be considered when a dependency fails.
- Container lifecycle and data lifecycle are different things.

## 7. Practical validation

To complete this lesson, verify that you can explain:

- Why services are separated.
- What happens when PostgreSQL fails.
- How the application behaves when Redis fails.
- Why PostgreSQL needs a persistent volume.
- How Docker Compose DNS allows services to communicate.

---

# Future lessons

| Lesson | Topic | Status |
|---|---|---|
| 02 | FastAPI application development | Pending |
| 03 | PostgreSQL integration | Pending |
| 04 | Redis integration | Pending |
| 05 | Docker fundamentals | Pending |
| 06 | Naive Dockerfile | Pending |
| 07 | Docker layers and caching | Pending |
| 08 | Multi-stage builds | Pending |
| 09 | Container security | Pending |
| 10 | Docker HEALTHCHECK | Pending |
| 11 | Docker Compose | Pending |
| 12 | Volumes and networks | Pending |
| 13 | Environment configuration | Pending |
| 14 | Security scanning | Pending |
| 15 | Performance measurements | Pending |
| 16 | Documentation and GitHub delivery | Pending |

## Lesson 02 — Building the FastAPI Application Locally

**Date:** 2026-11-05  
**Status:** In progress

## Engineering Lessons 
- Isolate Python dependencies with virtual environments. 
- Separate the API application from the ASGI server. 
- Understand HTTP methods and status codes. 
- Test endpoints with curl instead of relying only on the browser. 
- Design APIs with future compatibility in mind.

### 1. Objectives

- Create a local Python environment.
- Install FastAPI and Uvicorn.
- Understand the client-server HTTP request lifecycle.
- Build and test the first API endpoints.
- Understand HTTP status codes and API versioning.

### 2. Python Environment

Created and activated a virtual environment:

```bash
python3 -m venv .venv
ACTIVATE .venv  ==>  source .venv/bin/activate

###  Run server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

### 10. Task Creation — POST

Implemented:

`POST /api/v1/tasks`

Technologies:
- Pydantic BaseModel for request validation.
- HTTP POST for resource creation.
- HTTP 201 Created for successful creation.
- Temporary Python list for in-memory storage.

Example request:

```http
POST /api/v1/tasks
Content-Type: application/json
{
  "title": "Learn Docker",
  "description": "Understand Docker fundamentals"
}

### 12. Complete CRUD Implementation

Implemented the following REST API operations:

| Operation | HTTP Method | Endpoint |
|-----------|-------------|----------|
| Create | POST | `/api/v1/tasks` |
| Read all | GET | `/api/v1/tasks` |
| Read one | GET | `/api/v1/tasks/{task_id}` |
| Replace | PUT | `/api/v1/tasks/{task_id}` |
| Partial update | PATCH | `/api/v1/tasks/{task_id}` |
| Delete | DELETE | `/api/v1/tasks/{task_id}` |

### 13. Pydantic Validation

Created two Pydantic models:

- `TaskCreate`: validates data required to create a task.
- `TaskUpdate`: supports partial updates.

Used `model_dump()` to convert Pydantic models into dictionaries.

Used `exclude_unset=True` to update only the fields provided by the client.

### 14. HTTP Status Codes

| Status | Meaning | Usage |
|--------|---------|-------|
| 200 | OK | Successful GET, PUT or PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 404 | Not Found | Task does not exist |
| 422 | Unprocessable Content | Invalid request data |

### 15. Current Implementation Limitations

- Tasks are stored in a Python list.
- Data is lost when the application process restarts.
- `len(tasks) + 1` is not a reliable unique ID strategy after deletions.
- The application does not yet use a persistent database.

These limitations will be addressed in subsequent lessons using PostgreSQL.

```


## Lesson 03 — Automated Testing with pytest

### Objective
Implement automated API tests for the FastAPI Task Manager application.

### Tools and dependencies
- pytest 9.2.0: test framework
- httpx 0.28.1: HTTP client dependency
- FastAPI TestClient: simulate HTTP requests without starting Uvicorn

### Concepts learned

1. TestClient:
   - Sends HTTP requests directly to the FastAPI application.
   - No separate Uvicorn server is required.

2. Assertions:
   - assert response.status_code == 200
   - assert response.json() == expected_data

3. Test isolation:
   - pytest fixtures prepare and clean the test environment.
   - monkeypatch temporarily replaces the task ID counter.
   - Each test starts with an empty task list and an ID counter starting at 1.

4. Parametrized testing:
   - pytest.mark.parametrize executes one test function with multiple inputs.
   - Useful for testing validation errors and edge cases.

5. HTTP testing:
   - 200: successful GET/PUT/PATCH
   - 201: successful POST
   - 204: successful DELETE
   - 404: resource not found
   - 422: request validation error

### Test coverage

- Health check
- Task creation
- Invalid task payloads
- Retrieve all tasks
- Retrieve task by ID
- Update task using PUT
- Partial update using PATCH
- Delete task
- Nonexistent resource handling

### Commands used

Run all tests:
python -m pytest -v

Show shorter error tracebacks:
python -m pytest -v --tb=short

### Important engineering lessons

- Tests should be independent.
- Test both successful and unsuccessful scenarios.
- Test edge cases, not only normal behavior.
- Automated tests help detect regressions after code changes.
- In-memory storage is temporary and unsuitable for persistent production data.

### Result

16 automated test cases passed.

### Next lesson
PostgreSQL integration and persistent data storage.


# Lesson 05.14 — PostgreSQL Integration Testing with Pytest

## 1. Objective

Replace the previous in-memory API tests with integration tests using a dedicated PostgreSQL test database.

The goal is to test the actual FastAPI endpoints while ensuring that test data does not persist between tests.

## 2. Architecture

- FastAPI: application under test.
- TestClient: sends HTTP requests without starting Uvicorn.
- Pytest: test framework and fixture management.
- SQLAlchemy: database sessions and transaction management.
- PostgreSQL: dedicated test database `task_manager_test_db`.

The development database `task_manager_db` is not used by the test suite.

## 3. Pytest fixtures

### create_test_tables

Creates the ORM tables in the test database once per pytest session using:

`Base.metadata.create_all(bind=test_engine)`

### db_connection

Opens a database connection and an external transaction for each test.

At the end of the test, the external transaction is rolled back.

### db_session

Creates a SQLAlchemy session bound to the test connection.

Uses `join_transaction_mode="create_savepoint"` so that commits inside API routes do not commit the external transaction.

### client

Uses FastAPI `dependency_overrides` to replace the application's `get_db` dependency with the test session.

TestClient sends HTTP requests to the application.

## 4. Transaction isolation

Each test runs inside its own external transaction.

The API routes can execute `commit()` normally. SQLAlchemy uses savepoints, while the outer transaction remains controlled by the fixture.

At the end of the test:

- The SQLAlchemy session is closed.
- The external transaction is rolled back.
- The database connection is closed.

This prevents test records from persisting between tests.

Note: PostgreSQL identity sequences are not rolled back like ordinary table data. Tests must not assume that generated IDs always start at 1.

## 5. Tests performed

- Health check.
- Task creation.
- Invalid creation payloads.
- Retrieve all tasks.
- Retrieve a task by ID.
- Retrieve a nonexistent task.
- Complete task replacement using PUT.
- PUT on nonexistent task.
- Partial update using PATCH.
- PATCH on nonexistent task.
- Task deletion.

Parameterized validation tests cover five invalid payload cases.

Total: 15 test cases.

## 6. Verification

Command:

`python -m pytest -v`

Result:

- 15 passed
- 0 failed
- Execution time: 0.54 seconds

A Starlette deprecation warning concerning HTTPX was reported. It did not prevent the tests from passing.

## 7. Key concepts learned

- Pytest fixtures and fixture scopes.
- FastAPI dependency overrides.
- SQLAlchemy sessions and external transactions.
- Savepoints and transaction rollback.
- Integration testing with PostgreSQL.
- Isolation between development and test databases.


<!-- # DOCKER -->


## Lesson 05.15 — Docker Image Layers and Build Cache

### Objective
Understand Docker image layers and verify how Docker reuses cached build instructions.

### Concepts learned

- A Docker image is composed of successive filesystem layers.
- Docker can reuse previously built layers through its build cache.
- Each Dockerfile instruction can contribute to an image layer.
- Instruction order matters for build performance.

### Dockerfile optimization principle

Copy dependency files before application source code:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
```

This avoids reinstalling Python dependencies when only application source code changes.

### Practical experiment

1. Built the initial image `task-manager-api:v1`.
2. Rebuilt it without changing files.
3. Observed that Docker reused cached layers.
4. Added a comment to `app/main.py`.
5. Rebuilt the image.
6. Verified that:
   - `COPY requirements.txt` remained cached.
   - `RUN pip install` remained cached.
   - `COPY app ./app` was rebuilt.

### Key takeaway

Docker reuses unchanged layers and rebuilds affected layers. Proper Dockerfile instruction ordering reduces unnecessary work and improves CI/CD build performance.


