from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

# List of Postgres connection IDs registered in Airflow UI or ENV
CONNECTION_IDS = ['source_retail', 'source_accounts', 'source_logistics']

def test_connection(conn_id):
    def _inner():
        hook = PostgresHook(postgres_conn_id=conn_id)
        try:
            conn = hook.get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            print(f"[{conn_id}] Connection successful. Result:", result)
        except Exception as e:
            print(f"[{conn_id}] Connection failed:", e)
            raise
    return _inner

with DAG(
    dag_id="check_all_postgres_connections",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["connectivity", "postgres"]
) as dag:

    for conn_id in CONNECTION_IDS:
        PythonOperator(
            task_id=f"check_connection_{conn_id}",
            python_callable=test_connection(conn_id)
        )
