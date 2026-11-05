
# Architecture Decision Records (ADR)

This document records important technical and architectural decisions
made during the development of containerized-app.

The goal is to understand not only WHAT we choose, but WHY.

---

# ADR-001 — Three-Tier Application Architecture

**Status:** Accepted

## Context

We need to build a small application with an API, persistent storage,
and caching.

We considered two approaches:

- Running all services inside one environment.
- Separating services into independent containers.

## Decision

We chose three independent services:

- FastAPI
- PostgreSQL
- Redis

Each service will run in its own Docker container.

## Reasons

### 1. Isolation

Each service has its own runtime environment and dependencies.

A failure in Redis should not automatically terminate PostgreSQL
or the FastAPI process.

### 2. Independent maintenance

We can update PostgreSQL without rebuilding the FastAPI image.

### 3. Scalability

We can scale the backend independently when application traffic grows.

### 4. Portability

The application can be reproduced on another machine using
the same configuration and compatible images.

## Consequences

- More services to manage.
- Additional network configuration.
- More complex troubleshooting.
- Better separation of responsibilities.

---

# ADR-002 — FastAPI as Backend Framework

**Status:** Accepted

## Context

We need a lightweight Python framework to expose REST API endpoints.

## Decision

Use FastAPI.

## Reasons

- Python-based.
- Lightweight and suitable for this project.
- Automatic OpenAPI documentation.
- Type hints and request validation.
- Easy integration with PostgreSQL and Redis.

## Consequences

We need to manage Python dependencies and application configuration.

---

# ADR-003 — PostgreSQL as Primary Database

**Status:** Accepted

## Context

Our application needs reliable persistent storage for tasks.

## Decision

Use PostgreSQL as the primary relational database.

## Reasons

- SQL support.
- Transactions.
- Data integrity.
- Persistent storage.
- Mature ecosystem.

## Consequences

We must configure database credentials, connections,
persistent volumes, and health checks.

---

# ADR-004 — Redis as Cache

**Status:** Accepted

## Context

Repeated database queries can increase database load.

## Decision

Use Redis to cache frequently requested data.

## Reasons

- In-memory data access.
- Simple key-value storage.
- Fast read operations.
- TTL support for cache expiration.

## Consequences

- Cache invalidation must be implemented.
- Redis failures must be handled gracefully.
- PostgreSQL remains the source of truth.
- Cached data may be lost without affecting permanent records.

---

# ADR-005 — Docker Compose Networking

**Status:** Planned

## Context

The three services need to communicate without relying on fixed
container IP addresses.

## Decision

Use a dedicated Docker Compose network.

## Planned communication

- FastAPI → postgres:5432
- FastAPI → redis:6379
- Client → FastAPI through port 8000

## Consequences

Services will use Compose service names for internal DNS resolution.

---

# ADR-006 — PostgreSQL Data Persistence

**Status:** Planned

## Context

Container filesystems are not intended to be the permanent storage
location for important database records.

## Decision

Use a named Docker volume for PostgreSQL data.

## Consequences

Database records can survive container removal and recreation,
provided the volume is preserved.

---

# Future decisions

Additional decisions will be documented as the architecture evolves:

- Docker base image selection.
- Multi-stage build strategy.
- Non-root container user.
- Container health checks.
- Environment variables and secrets.
- Resource limits.
- Image security scanning.

