
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
source .venv/bin/activate
