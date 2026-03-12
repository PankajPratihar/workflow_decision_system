# Configurable Workflow Decision Platform

A **configurable workflow decision system** built using FastAPI that processes incoming requests, evaluates rules, executes workflow stages, maintains state, and provides complete audit trails.

This system demonstrates how business workflows such as **payments, claims, approvals, and verification processes** can be automated using a configurable rules engine.

---

## Project Overview

The platform accepts structured requests through an API or UI, evaluates configurable rules, and determines the correct workflow outcome such as:

* Approve
* Reject
* Retry
* Manual Review

It also records every step in an **audit trail** to ensure transparency and explainability of decisions.

---

## Key Features

* Configurable **rules engine**
* Dynamic **workflow execution**
* **Audit trail logging**
* **State management** for request lifecycle
* **Idempotent request handling**
* **Decision explanation** showing triggered rules
* **REST API** using FastAPI
* **PostgreSQL / SQLite database support**
* **Docker containerization**
* Interactive **UI dashboard for workflow execution**

---

## System Architecture

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
Workflow Engine
      |
      v
Database (PostgreSQL / SQLite)
      |
      v
Audit Logs + Decision History
```

---

## Project Structure

```
workflow-decision-platform
│
├── app
│   ├── api
│   │   └── routes.py
│   ├── core
│   │   ├── rules_engine.py
│   │   └── workflow_engine.py
│   ├── models
│   ├── services
│   └── config
│
├── database
│
├── frontend
│
├── tests
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── architecture.md
```

---

## Workflow Configuration Example

Workflows are defined using a JSON configuration file.

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

This allows workflow logic to be updated **without changing the application code**.

---

## API Endpoints

### Execute Workflow

```
POST /execute
```

Example request:

```json
{
 "request_id": "req_5838",
 "workflow_id": "payment_workflow",
 "amount": 50000,
 "currency": "USD"
}
```

Example response:

```json
{
 "status": "completed",
 "decision": "manual_review",
 "triggered_rule": "amount > 1000"
}
```

---

### Decision History

```
GET /decision/{request_id}
```

Returns decision history and audit trail for a request.

---

## Audit Trail Example

```
12:36:59 INITIALIZATION  Starting workflow
12:36:59 DECISION        Rule evaluation result: manual_review
12:36:59 EXECUTION       Executing manual review logic
12:36:59 COMPLETION      Workflow finished successfully
```

---

## Running the Project (Local)

Install dependencies:

```
pip install -r requirements.txt
```

Start the server:

```
uvicorn app.main:app --reload
```

Open the API docs:

```
http://127.0.0.1:8000/docs
```

---

## Running with Docker

Make sure Docker is installed.

Start the platform:

```
docker-compose up --build
```

Access the application:

```
http://localhost:3000
```

The system will automatically start:

* FastAPI application
* PostgreSQL database

---

## Database

The system supports two databases:

* SQLite (local development)
* PostgreSQL (production via Docker)

Tables include:

* Requests
* Audit Logs
* Processed Requests (for idempotency)

---

## Testing

Run tests using:

```
pytest
```

Test scenarios include:

* Valid workflow execution
* Invalid input validation
* Duplicate request handling
* Rule evaluation correctness
* Failure and retry scenarios

---

## Scalability Considerations

Future improvements may include:

* Distributed workflow workers
* Message queues (RabbitMQ / Kafka)
* Redis caching
* Rule versioning
* Horizontal API scaling

---

## Technologies Used

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* SQLite
* Docker
* JavaScript / HTML UI

---

## Author

Pankaj Pratihar
BTech – Metallurgy and Materials Engineering

---

## License

This project is for **educational and hackathon purposes**.
