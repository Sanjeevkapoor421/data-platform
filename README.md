# Data Platform

A lightweight local data platform for ingesting, storing, and serving data — built with Python, Airflow, PostgreSQL, and Docker.

## What's inside

| Layer | Tech | Purpose |
|---|---|---|
| **App** | FastAPI | REST API to serve data |
| **Ingestion** | Apache Airflow | Daily ETL pipelines to load CSV data into PostgreSQL |
| **Storage** | PostgreSQL + Flyway | Relational database with versioned schema migrations |
| **Infrastructure** | Docker Compose | Spin up all services locally |

## Project Structure

```
data-platform/
├── app/                        # FastAPI application
├── data-ingestion/             # Airflow DAGs and ETL scripts
│   └── dags/                   # ETL pipeline (users & products)
├── storage/                    # PostgreSQL setup
│   └── migrations/             # Flyway SQL migrations
└── deploy/                     # Deployment configs (Airflow Helm values)
```

## Getting Started

**Start the database:**
```bash
cd storage
docker compose up -d
```

**Start Airflow:**
```bash
cd data-ingestion
docker compose up -d
```

**Run the API:**
```bash
cd app
uvicorn main:app --reload
```

## Deploying Airflow to Kubernetes

The `deploy/airflow/` folder contains Helm chart configs to deploy Airflow on a Kubernetes cluster.

**Prerequisites:** `kubectl` and `helm` installed and pointed at your cluster.

```bash
cd deploy/airflow
bash install.sh
```

This will:
1. Add the Apache Airflow Helm repo
2. Apply the connections secret to Kubernetes
3. Install Airflow (chart version 1.14.0, image 2.9.1) in the `airflow` namespace

**Access the UI after deploy:**
```bash
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
```
Then open http://localhost:8080.

> Before deploying, update `values-override.yaml` with your Postgres host and a real `webserverSecretKey`.

## Data Model

- **users** — registered users
- **products** — product catalog with pricing and stock
- **orders** — user orders with status tracking
- **order_items** — line items per order
