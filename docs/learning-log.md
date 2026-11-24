
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
# DOCKER conrainer

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



## Lesson 05.16 — Docker Compose, Networking and Persistent Volumes

### Objective

Understand how multiple containers communicate, how service readiness is checked, and how Docker preserves database data beyond container removal.

### Architecture

The application uses two separate services:

- `api`: FastAPI application.
- `db`: PostgreSQL database.

Docker Compose creates a shared network for these services.

The API connects to PostgreSQL using the service name `db` and internal port `5432`.

### Concepts learned

- Docker Compose creates a network for the application services.
- Containers can communicate using service names through Docker DNS.
- A container's lifecycle is independent of the data stored in a named volume.
- A healthcheck verifies whether a service is ready.
- `depends_on` with `condition: service_healthy` controls startup ordering based on service health.

### Persistent volume experiment

1. Created a task through the FastAPI API.
2. Verified that the task was stored in PostgreSQL.
3. Ran `docker compose down` to remove containers and the Compose network.
4. Recreated the services using `docker compose up -d`.
5. Verified that PostgreSQL became healthy.
6. Retrieved the task again through the API.

The task was still present after the containers were recreated.

### Important distinction

- `docker compose down`: removes containers and the Compose network, but preserves named volumes by default.
- `docker compose down -v`: also removes Compose-managed named volumes.

The second command can permanently delete the database data stored in those volumes.

### Key takeaway

Containers are replaceable, but persistent data must be stored outside the container's writable filesystem.

Docker Compose networking, healthchecks, service dependencies, and named volumes are essential concepts for running multi-container applications reliably.


## Lesson 05.16 — Docker Compose, Networking and Persistent Volumes

### Objective

- Multi-container architecture : l'API FastAPI et PostgreSQL fonctionnent dans deux conteneurs distincts.
- Docker networking : l'API utilise db comme nom d'hôte pour joindre PostgreSQL sur le port 5432. Docker Compose fournit la résolution DNS entre services.
- Healthcheck : PostgreSQL utilise pg_isready pour vérifier qu'il est prêt à accepter des connexions.
- depends_on : condition: service_healthy permet d'attendre que PostgreSQL soit opérationnel avant de démarrer l'API.
- Named volume : postgres_data conserve les données indépendamment du cycle de vie du conteneur.

Understand how multiple containers communicate, how service readiness is checked, and how Docker preserves database data beyond container removal.

### Architecture

The application uses two separate services:

- `api`: FastAPI application.
- `db`: PostgreSQL database.

Docker Compose creates a shared network for these services.

The API connects to PostgreSQL using the service name `db` and internal port `5432`.

### Concepts learned

- Docker Compose creates a network for the application services.
- Containers can communicate using service names through Docker DNS.
- A container's lifecycle is independent of the data stored in a named volume.
- A healthcheck verifies whether a service is ready.
- `depends_on` with `condition: service_healthy` controls startup ordering based on service health.

### Persistent volume experiment

1. Created a task through the FastAPI API.
2. Verified that the task was stored in PostgreSQL.
3. Ran `docker compose down` to remove containers and the Compose network.
4. Recreated the services using `docker compose up -d`.
5. Verified that PostgreSQL became healthy.
6. Retrieved the task again through the API.

The task was still present after the containers were recreated.

### Important distinction

- `docker compose down`: removes containers and the Compose network, but preserves named volumes by default.
- `docker compose down -v`: also removes Compose-managed named volumes.

The second command can permanently delete the database data stored in those volumes.

### Key takeaway

Containers are replaceable, but persistent data must be stored outside the container's writable filesystem.

Docker Compose networking, healthchecks, service dependencies, and named volumes are essential concepts for running multi-container applications reliably.


---

## Docker Image Optimization and Security

### 1. Understanding Docker Image Layers

A Docker image is composed of multiple read-only layers. Each Dockerfile instruction that changes the image filesystem can create a new layer.

We inspected the image using:

```bash
docker image inspect task-manager-api:v1
docker history task-manager-api:v1
```

We also examined directory sizes inside the container:

```bash
du -sh /usr/local/lib/python3.12/site-packages/*
du -h -d 2 /usr/local/lib/python3.12/site-packages/sqlalchemy
```

**Concepts learned:**

- Docker layers are reused during image builds.
- Each layer contributes to the image size.
- `docker history` helps identify which instructions create large layers.
- `docker image inspect` provides image metadata, including its size.
- `du` helps identify which directories and packages consume disk space.

**Key takeaway:**

Image optimization starts with measurement. We should identify where the space is being used before modifying the Dockerfile.

### 2. Docker Build Context and `.dockerignore`

We created and improved a `.dockerignore` file to prevent unnecessary files from being sent to the Docker build context.

The file excludes:

- Environment files such as `.env`.
- Python virtual environments.
- Python cache files (`__pycache__`, `.pyc`, `.pyo`).
- Test artifacts and coverage reports.
- Git metadata.
- Documentation and local backup files.

**Concepts learned:**

- The build context contains the files Docker can access during a build.
- `.dockerignore` excludes unnecessary or sensitive files from that context.
- Excluding `.env` helps prevent accidental inclusion of secrets in the image.
- Smaller build contexts reduce unnecessary data transfer and help keep builds clean.

**Verification:**

We inspected the files inside the resulting container and confirmed that unnecessary backup files and Python cache files were not copied into the application image.

### 3. Running Containers as a Non-Root User

Initially, the application ran using the default user, which is typically root in the base image.

We created a dedicated system group and user:

```dockerfile
RUN groupadd --system app \
    && useradd --system \
        --gid app \
        --no-create-home \
        --shell /usr/sbin/nologin \
        app
```

We changed ownership of the application files:

```dockerfile
COPY --chown=app:app app ./app
```

We then configured the runtime user:

```dockerfile
USER app
```

**Concepts learned:**

- Containers do not need to run as root for most application workloads.
- The principle of least privilege reduces the impact of a compromised application.
- `USER` defines the user used by subsequent runtime instructions.
- `COPY --chown` assigns file ownership during the image build.
- `--no-create-home` avoids creating an unnecessary home directory.
- `/usr/sbin/nologin` prevents normal interactive login for the system account.

**Verification:**

We inspected the image configuration:

```bash
docker image inspect task-manager-api:v1 \
  --format 'Configured user: {{.Config.User}}'
```

We also checked the effective user inside a container:

```bash
docker compose run --rm --no-deps api id
```

The application ran using the dedicated `app` user instead of root.

### 4. Multi-Stage Docker Builds

We created a separate Dockerfile named `Dockerfile.multistage`.

The objective was to separate dependency installation from the final runtime image.

**Builder stage:**

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

**Runtime stage:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd --system app \
    && useradd --system \
        --gid app \
        --no-create-home \
        --shell /usr/sbin/nologin \
        app

COPY --from=builder /install /usr/local

COPY --chown=app:app app ./app

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build command:

```bash
docker build -f Dockerfile.multistage \
  -t task-manager-api:multistage .
```

**Concepts learned:**

- Multi-stage builds use multiple `FROM` instructions.
- The builder stage prepares dependencies.
- The runtime stage receives only the files copied from the builder and the application source.
- `COPY --from=builder` transfers selected files between stages.
- Build-time and runtime responsibilities can be separated.

**Important observation:**

The multi-stage image did not significantly reduce the final image size because both stages used the same Python base image and the runtime still needed all application dependencies.

Multi-stage builds are useful, but they do not automatically guarantee a smaller image.

### 5. Python Dependency Installation Optimization

We investigated the size of Python packages and discovered that Python bytecode compilation contributed to the image size.

We added `--no-compile` to the dependency installation command:

```dockerfile
RUN pip install \
    --no-cache-dir \
    --no-compile \
    --prefix=/install \
    -r requirements.txt
```

**Concepts learned:**

- `--no-cache-dir` prevents pip from retaining its download cache.
- `--no-compile` prevents pip from compiling installed Python modules into `.pyc` files during installation.
- `PYTHONDONTWRITEBYTECODE=1` prevents Python from writing bytecode files during normal execution.
- These two options have different purposes: one concerns pip installation, the other Python runtime behavior.

We created a new image:

```bash
docker build -f Dockerfile.multistage \
  -t task-manager-api:optimized-no-compile .
```

### 6. Image Size Comparison

We compared the three images using:

```bash
docker image inspect \
  task-manager-api:v1 \
  task-manager-api:multistage \
  task-manager-api:optimized-no-compile \
  --format '{{.RepoTags}} : {{.Size}} bytes'
```

Measured results:

| Image | Size |
|---|---:|
| `task-manager-api:v1` | 267,619,417 bytes |
| `task-manager-api:multistage` | 267,607,209 bytes |
| `task-manager-api:optimized-no-compile` | 243,262,609 bytes |

The optimized image reduced the size by:

- 24,356,808 bytes.
- Approximately 24.36 MB (decimal).
- Approximately 9.1% compared with the original image.

**Key takeaway:**

The significant improvement came from disabling bytecode compilation during dependency installation, rather than simply introducing multi-stage builds.

### 7. Image Validation

We verified that the optimized image contained the required Python dependencies:

```bash
docker run --rm \
  --entrypoint python \
  task-manager-api:optimized-no-compile \
  -c "import fastapi, sqlalchemy, psycopg; print('Dependencies OK')"
```

We also checked the configured runtime user:

```bash
docker image inspect task-manager-api:optimized-no-compile \
  --format 'Configured user: {{.Config.User}}'
```

The checks confirmed:

- FastAPI, SQLAlchemy and psycopg could be imported.
- The configured user was `app`.

The optimized image passed these checks. A full end-to-end test against PostgreSQL using this exact image remains a separate validation step.

### 8. Additional Investigation: Removing pip

We investigated whether removing pip from the final image would provide additional savings.

We found that pip was already included in the Python base image.

**Concepts learned:**

- Docker uses a layered filesystem.
- Deleting a file in a later layer does not necessarily remove the bytes stored in an earlier image layer.
- Removing inherited files can therefore hide them without recovering the original layer's storage.
- Building a custom Python runtime to remove inherited tools adds complexity and should be justified by measurable benefits.

**Decision:**

We did not modify the runtime to remove pip because the expected benefit was limited compared with the additional complexity.

### Overall Lessons

- Measure image size before and after each optimization.
- Use `.dockerignore` to keep the build context clean and exclude secrets.
- Run application containers as non-root users.
- Understand that multi-stage builds separate build and runtime environments but do not guarantee smaller images.
- Optimize Python dependency installation with the appropriate pip options.
- Validate image functionality after each change.
- Avoid optimizations that add complexity without a meaningful benefit.

**Next topic:** Container image vulnerability scanning with Trivy.

### 8. Runtime Hardening: Removing pip

We investigated the presence of pip in the final runtime image.

Pip was inherited from the official Python base image. Since the application only needs its installed runtime dependencies, pip is not required to start FastAPI.

**Implementation:**

After copying the installed dependencies from the builder stage, we removed pip from the runtime image:

```dockerfile
COPY --from=builder /install /usr/local
RUN python -m pip uninstall -y pip
```

**Verification:**

- `python -m pip --version` confirmed that pip was no longer available.
- Imports of FastAPI, SQLAlchemy, psycopg and Uvicorn succeeded.
- The application continued to start correctly.

After removing pip, Trivy no longer reported the six Python findings previously associated with pip metadata.

**Concepts learned:**

- A runtime image should contain what the application needs to run, not necessarily all the tools used during development or installation.
- Multi-stage builds allow dependencies to be installed in a builder stage and copied into the runtime stage.
- Removing an unnecessary runtime tool can reduce the attack surface.
- Changes to the runtime must be followed by application and dependency verification.

### 9. Container Image Security Scanning with Trivy

We installed Trivy and used it to scan the Docker images for known vulnerabilities.

The goal was to understand the image's security posture, identify vulnerable packages and distinguish between vulnerabilities with available fixes and vulnerabilities that could not yet be fixed through the configured package repositories.

#### Initial scan

The first full scan of the optimized image reported:

- Debian OS packages: 240 findings.
- Python packages: 6 findings, associated with pip.
- No CRITICAL findings.

The scan showed that most findings came from the Debian base image and its system packages, rather than from the application's Python dependencies.

#### Fixing the zlib vulnerability

A HIGH vulnerability, CVE-2026-85091, was identified in `zlib1g` with an available fix.

We installed the corrected package in the runtime stage:

```dockerfile
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends zlib1g \
    && rm -rf /var/lib/apt/lists/*
```

The rebuilt image contained the corrected zlib package version:

`1:1.3.dfsg+really1.3.1-1+deb13u1`

A subsequent Trivy scan confirmed that the zlib finding had disappeared.

#### Updating Debian packages

We investigated the remaining HIGH findings using an APT upgrade simulation:

```bash
docker run --rm \
  --user root \
  --entrypoint sh \
  task-manager-api:optimized-no-compile \
  -c 'apt-get update -qq && apt-get -s upgrade'
```

The simulation identified available updates for packages including:

- `base-files`
- `libc6` and `libc-bin`
- `libssl3t64`
- `openssl`
- `openssl-provider-legacy`

We integrated `apt-get upgrade -y` into the runtime build and rebuilt the image.

We then verified the installed package versions and compared them with the available APT candidates.

Some remaining vulnerable packages had no newer candidate versions in the configured Debian repositories at the time of the investigation.

#### Understanding unfixed vulnerabilities

After the updates, Trivy still reported HIGH findings for several Debian packages, including:

- util-linux
- libacl
- ncurses
- SQLite
- systemd
- perl-base

The remaining findings did not all have an available fix in the configured repositories.

We also ran a filtered scan:

```bash
trivy image \
  --scanners vuln \
  --severity HIGH,CRITICAL \
  --ignore-unfixed \
  task-manager-api:optimized-no-compile
```

This returned zero HIGH or CRITICAL findings with known fixes.

**Important:** This does not mean that the image contains zero vulnerabilities. The `--ignore-unfixed` option excludes vulnerabilities for which Trivy does not identify an available fix. The remaining unfixed findings must still be documented and monitored.

**Concepts learned:**

- A vulnerability scanner identifies known security issues in operating-system and application packages.
- A HIGH or CRITICAL severity does not automatically mean that a fix is available.
- `apt-get upgrade` can only install versions available in the configured repositories.
- `--ignore-unfixed` is useful for prioritizing actionable vulnerabilities, but it must not be interpreted as proof that an image is vulnerability-free.
- Security scanning is an iterative process: scan, investigate, update, rebuild and scan again.

### 10. Final Validation of the Optimized Image

After hardening the image, we tested the exact optimized image in a separate container without replacing the existing API container or recreating PostgreSQL.

The test container was launched with:

- Image: `task-manager-api:optimized-no-compile`
- Container: `containerized-app-api-optimized-test`
- Host port: `8001`
- Container port: `8000`
- Docker network: `containerized-app_default`
- Runtime user: `app`

The test container reused the database environment configuration of the existing API container without displaying database credentials.

**Functional checks:**

- `GET /health` returned HTTP 200 OK.
- `GET /api/v1/info` returned HTTP 200 OK.
- `GET /api/v1/tasks` returned HTTP 200 OK and successfully accessed PostgreSQL.

The optimized API and the original API ran simultaneously on separate host ports.

The tests did not require recreating the PostgreSQL container, deleting its volume or modifying existing database records.

This confirmed that the optimized image could start the application and communicate with the existing PostgreSQL service.

### 11. Image Size Analysis

We compared the final image sizes:

| Image | Size |
|---|---:|
| `task-manager-api:v1` | 267,619,417 bytes |
| `task-manager-api:multistage` | 267,607,209 bytes |
| `task-manager-api:optimized-no-compile` | 280,882,156 bytes |

We also compared the Python dependency directories:

| Image | `site-packages` size |
|---|---:|
| Classic image | 75 MB |
| Optimized image | 50 MB |

This represents a reduction of approximately 33.3% in the space occupied by Python dependencies.

However, the final optimized image was approximately 13.26 MB larger than the classic image.

The investigation showed that the multi-stage build reduced the Python dependency footprint, while the Debian package upgrades and additional runtime packages increased the total image size.

**Conclusion:**

A multi-stage build does not automatically guarantee a smaller final image. Image size must be measured after all runtime security updates and hardening steps have been included.

We decided to prioritize a functional and hardened runtime over removing system packages solely to reduce image size.

### Overall Lessons

- Measure image size before and after each optimization.
- Use `.dockerignore` to keep the build context clean and exclude secrets.
- Use multi-stage builds to separate dependency installation from the runtime environment.
- Run application containers as non-root users.
- Remove unnecessary runtime tools only when their removal is justified and verified.
- Understand Docker image layers and why deleting files in later layers does not necessarily recover space from earlier layers.
- Use Trivy to identify vulnerabilities in both OS packages and application dependencies.
- Distinguish fixed vulnerabilities from unfixed vulnerabilities.
- Never interpret a scan using `--ignore-unfixed` as proof that an image is vulnerability-free.
- Rebuild and rescan after applying security updates.
- Validate application startup, API endpoints and database connectivity after modifying the runtime image.
- Preserve existing database volumes and data during container testing.
- Prefer measurable and justified optimizations over unnecessary complexity.

**Next topic:** Redis integration and caching in the Task Manager application.


