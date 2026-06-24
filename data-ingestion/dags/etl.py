import csv
from pathlib import Path

import psycopg2
from airflow.hooks.base import BaseHook

# ── Change this to target a different database ──────────────────────────────
CUST_SLUG = "sanjeev"
# ────────────────────────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent.parent / "data"


def get_connection():
    conn_id = f"postgres_{CUST_SLUG}"
    conn = BaseHook.get_connection(conn_id)
    return psycopg2.connect(
        host=conn.host,
        port=conn.port or 5432,
        dbname=conn.schema,
        user=conn.login,
        password=conn.password,
    )


def load_users(cur):
    with open(DATA_DIR / "users.csv") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        cur.execute(
            """
            INSERT INTO users (email, name)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING
            """,
            (row["email"], row["name"]),
        )

    print(f"  users: {len(rows)} rows processed")


def load_products(cur):
    with open(DATA_DIR / "products.csv") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        cur.execute(
            """
            INSERT INTO products (name, price, stock)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (row["name"], float(row["price"]), int(row["stock"])),
        )

    print(f"  products: {len(rows)} rows processed")


def run():
    conn_id = f"postgres_{CUST_SLUG}"
    print(f"ETL → {CUST_SLUG} (conn_id={conn_id})")

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                load_users(cur)
                load_products(cur)
        print("Done.")
    finally:
        conn.close()


if __name__ == "__main__":
    run()
