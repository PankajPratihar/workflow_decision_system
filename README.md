# Configurable Workflow Decision Platform

A **configurable workflow decision system** built using FastAPI that processes incoming requests, evaluates rules, executes workflow stages, maintains state, and provides complete audit trails.

This system demonstrates how business workflows such as **payments, claims processing, approvals, and verification workflows** can be automated using a configurable rules engine.

---

# Project Overview

The platform accepts structured workflow requests via a REST API or UI, evaluates configurable rules, and determines the correct workflow outcome.

Possible workflow outcomes:

* Approve
* Reject
* Retry
* Manual Review

Each workflow execution generates a **complete audit trail**, ensuring transparency, traceability, and explainability of decisions.

---

# Key Features

* Configurable **Rules Engine**
* Dynamic **Workflow Execution Engine**
* **Audit Trail Logging**
* **State Management** for request lifecycle
* **Idempotent Request Handling**
* **Retry Logic for External Failures**
* **Decision Explanation with Triggered Rule**
* **REST API using FastAPI**
* **PostgreSQL / SQLite database support**
* **Docker containerization**
* Interactive **UI dashboard**

---

# System Architecture

```
Client / UI
      |
      v
FastAPI REST API
      |
      v
Request Validation
      |
      v
Rules Engine
      |
      v
Workflow Orchestrator
      |
      v
State Manager + Idempotency Store
      |
      v
Database (SQLite / PostgreSQL)
      |
      v
Audit Logs + Decision History
```

For a detailed architecture explanation see:

```
ARCHITECTURE.md
```

---

# Project Structure

```
workflow_decision_system
│
├── backend
├── src
│
├── main.py
├── database.py
├── db_models.py
├── models.py
├── workflow_models.py
│
├── rules_engine.py
├── workflow_engine.py
├── services.py
│
├── rules_config.json
│
├── example_queries.py
├── workflow_demo.py
├── test_workflow.py
│
├── docker-compose.yml
├── Dockerfile
├── DOCKER_INSTRUCTIONS.md
│
├── ARCHITECTURE.md
├── README.md
│
├── index.html
│
├── metadata.json
│
├── package.json
├── vite.config.ts
├── server.ts
```

---

# Workflow Configuration Example

Workflows are configured using a JSON rule definition.

Example:

```json
{
 "id": "payment_workflow",
 "rules": [
   { "condition": "amount == 777", "action": "retry" },
   { "condition": "amount > 1000", "action": "manual_review" },
   { "condition": "currency != 'USD'", "action": "reject" },
   { "condition": "true", "action": "approve" }
 ]
}
```

This allows business rules to be modified **without changing application code**.

---

# API Endpoints

## Process Workflow Request

```
POST /process_request
```

Example request:

```json
{
 "request_id": "req_100",
 "payload": {
   "amount": 50000,
   "currency": "USD"
 }
}
```

Example response:

```json
{
 "request_id": "req_100",
 "status": "approved",
 "result": {
   "message": "External processing successful"
 },
 "audit_trail": [
   {
     "event": "WORKFLOW_STARTED"
   },
   {
     "event": "EXTERNAL_CALL_ATTEMPT"
   }
 ]
}
```

---

## Decision History

```
GET /decision/{request_id}
```

Returns decision history and audit trail for a workflow request.

---

# Audit Trail Example

```
WORKFLOW_STARTED
EXTERNAL_CALL_ATTEMPT
EXTERNAL_CALL_FAILURE
RETRY_WAIT
WORKFLOW_COMPLETED
```

This enables **complete traceability of workflow decisions**.

---

# Running the Project Locally

### Install Dependencies

```
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

### Start the FastAPI Server

```
uvicorn main:app --reload
```

### Open API Documentation

```
http://127.0.0.1:8000/docs
```

---

# Running with Docker

Ensure Docker is installed.

Start the platform:

```
docker-compose up --build
```

This launches:

* FastAPI backend
* PostgreSQL database

Access the application:

```
http://localhost:3000
```

---

# Database

The platform supports two databases:

* **SQLite** (local development)
* **PostgreSQL** (Docker deployment)

Tables include:

* Requests
* Audit Logs
* Processed Requests (Idempotency)

---

# Testing

Run automated tests:

```
pytest
```

Test cases include:

* Workflow execution
* Rule evaluation
* Idempotent request handling
* Retry logic
* Failure scenarios

---

# Scalability Considerations

Future improvements could include:

* Distributed workflow workers
* Message queues (RabbitMQ / Kafka)
* Redis caching
* Rule versioning
* Horizontal API scaling

---

# Technologies Used

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* SQLite
* Docker
* HTML / JavaScript

---

# Author

**Pankaj Pratihar**
BTech – Metallurgy and Materials Engineering
NIT Rourkela

---

# License

This project is created for **educational and hackathon demonstration purposes**.
