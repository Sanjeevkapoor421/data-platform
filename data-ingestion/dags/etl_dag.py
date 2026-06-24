from datetime import datetime

import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator

from etl import DATA_DIR, DB_MAP, CUST_SLUG, load_users, load_products

with DAG(
    dag_id="etl_csv_to_postgres",
    description="Load users and products CSVs into the target customer database",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", CUST_SLUG],
) as dag:

    def _get_conn_kwargs():
        if CUST_SLUG not in DB_MAP:
            raise ValueError(f"Unknown CUST_SLUG '{CUST_SLUG}'. Valid: {list(DB_MAP)}")
        return DB_MAP[CUST_SLUG]

    def task_load_users():
        conn = psycopg2.connect(**_get_conn_kwargs())
        try:
            with conn:
                with conn.cursor() as cur:
                    load_users(cur)
        finally:
            conn.close()

    def task_load_products():
        conn = psycopg2.connect(**_get_conn_kwargs())
        try:
            with conn:
                with conn.cursor() as cur:
                    load_products(cur)
        finally:
            conn.close()

    load_users_task = PythonOperator(
        task_id="load_users",
        python_callable=task_load_users,
    )

    load_products_task = PythonOperator(
        task_id="load_products",
        python_callable=task_load_products,
    )

    load_users_task >> load_products_task
