#!/usr/bin/env bash
set -e

# Add the Apache Airflow Helm repo
helm repo add apache-airflow https://airflow.apache.org
helm repo update

# Apply the connections secret first
kubectl apply -f "$(dirname "$0")/secrets/airflow-connections.yaml"

# Install / upgrade
helm upgrade --install airflow apache-airflow/airflow \
  --version 1.14.0 \
  --namespace airflow \
  --create-namespace \
  -f "$(dirname "$0")/values-override.yaml"

echo ""
echo "Airflow deployed. Port-forward the webserver with:"
echo "  kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow"
