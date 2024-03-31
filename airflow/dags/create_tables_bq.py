import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

PROJECT_ID = os.getenv('PROJECT_ID')
DATASET_NAME = os.getenv('DATASET_NAME')
EXTERNAL_TABLE_NAME = 'ext_bikeshare'
PARTITIONED_TABLE_NAME = 'prt_bikeshare'
BUCKET_NAME = os.getenv('BUCKET_NAME')
PATH_TO_FILES = 'capital-bikeshare-data/*.csv'

with DAG('create_base_tables',
         default_args=default_args,
         description='Crate a external table in BigQuery from a folder into a Bucket and then a partitioned table based.',
         schedule_interval=timedelta(days=1),
         catchup=False) as dag:

    create_external_table = BigQueryInsertJobOperator(
        task_id='create_external_table',
        configuration={
            'query': {
                'query': f'''CREATE OR REPLACE EXTERNAL TABLE `{PROJECT_ID}.{DATASET_NAME}.{EXTERNAL_TABLE_NAME}`
                            OPTIONS (
                            format = 'csv',
                            uris = ['gs://{BUCKET_NAME}/{PATH_TO_FILES}']
                            );''',
                'useLegacySql': False,
            }
        },
    )

    create_partitioned_table = BigQueryInsertJobOperator(
        task_id='create_partitioned_table',
        configuration={
            'query': {
                'query': f'''CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_NAME}.{PARTITIONED_TABLE_NAME}`
                            PARTITION BY started_at_date
                            AS SELECT * FROM `{PROJECT_ID}.{DATASET_NAME}.{EXTERNAL_TABLE_NAME}`''',
                'useLegacySql': False,
            },
        },
    )

    create_external_table >> create_partitioned_table