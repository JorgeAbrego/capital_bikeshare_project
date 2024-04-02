from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('master_dag',
         default_args=default_args,
         #schedule_interval=timedelta(days=1),
         schedule_interval='0 23 * * *',
         catchup=False) as dag:

    trigger_load_datalake = TriggerDagRunOperator(
        task_id='trigger_load_datalake',
        trigger_dag_id='extracting_and_loading', 
        wait_for_completion=True,
        poke_interval=30,
    )

    trigger_create_tables = TriggerDagRunOperator(
        task_id='trigger_create_tables',
        trigger_dag_id='create_base_tables',
        wait_for_completion=True,
        poke_interval=30, 
    )

    trigger_run_dbt_container = TriggerDagRunOperator(
        task_id='trigger_run_dbt_container',
        trigger_dag_id='dbt_run_project', 
        wait_for_completion=True,
        poke_interval=30,
    )

    trigger_load_datalake >> trigger_create_tables >> trigger_run_dbt_container