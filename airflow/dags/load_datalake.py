import os
import pandas as pd
import requests
import zipfile
from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from google.cloud import storage

BUCKET_NAME = os.getenv('BUCKET_NAME')

def determine_year_month(**kwargs):
    try:
        year_month = Variable.get("year_month")
    except KeyError:
        year_month = kwargs['ds_nodash'][:6]  # Use the execution date if the variable is not set
    return year_month

def download_zip_file(year_month, destination_folder='data-downloads', **kwargs):
    url = f"https://s3.amazonaws.com/capitalbikeshare-data/{year_month}-capitalbikeshare-tripdata.zip"
    print(f"Downloading from {url}")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    file_name = url.split('/')[-1]
    full_path = os.path.join(destination_folder, file_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(full_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved in: {full_path}")
    else:
        raise Exception(f"Error downloading the file. Status code: {response.status_code}")

def extract_csv(year_month, destination_folder='data-downloads', **kwargs):
    zip_file_name = f"{year_month}-capitalbikeshare-tripdata.zip"
    zip_base_name = os.path.splitext(zip_file_name)[0] 
    zip_path = os.path.join(destination_folder, zip_file_name)
    extracted_csv_file_name = None 
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.csv') and not file.startswith('_MACOSX'):
                zip_ref.extract(file, destination_folder)
                original_csv_name = os.path.splitext(file)[0] 
                if original_csv_name != zip_base_name:
                    new_csv_name = zip_base_name + '.csv'
                    os.rename(os.path.join(destination_folder, file),
                              os.path.join(destination_folder, new_csv_name))
                    extracted_csv_file_name = new_csv_name
                else:
                    extracted_csv_file_name = file
                print(f"CSV file {extracted_csv_file_name} extracted in: {destination_folder}")
                break 

    if extracted_csv_file_name is None:
        raise Exception(f"No valid CSV file found in the zip file {zip_file_name}.")

def transform_data(year_month, destination_folder='data-downloads', **kwargs):
    csv_file_name = f"{year_month}-capitalbikeshare-tripdata.csv"
    csv_path = os.path.join(destination_folder, csv_file_name)
    df = pd.read_csv(csv_path)
    df.dropna(subset=['start_station_id', 'end_station_id'], inplace=True)
    df['start_station_id'] = df['start_station_id'].astype(int)
    df['end_station_id'] = df['end_station_id'].astype(int)
    df['started_at_date'] = pd.to_datetime(df['started_at']).dt.date
    df.to_csv(csv_path, index=False)
    print(f"Transformed data saved to: {csv_path}")

def upload_to_gcs(bucket_name, year_month, destination_folder='data-downloads', **kwargs):
    source_file_name = f"{year_month}-capitalbikeshare-tripdata.csv"
    destination_blob_name = f"capital-bikeshare-data/{year_month}-capitalbikeshare-tripdata.csv"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(os.path.join(destination_folder, source_file_name))
    print(f"File uploaded to: {destination_blob_name}.")

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('extracting_and_loading', default_args=default_args, schedule_interval='@monthly', catchup=False) as dag:
    determine_year_month_task = PythonOperator(
        task_id='determine_year_month',
        python_callable=determine_year_month,
        provide_context=True,
        op_kwargs={'ds_nodash': '{{ ds_nodash }}'}
    )

    download_zip = PythonOperator(
        task_id='download_zip',
        python_callable=download_zip_file,
        op_args=['{{ task_instance.xcom_pull(task_ids="determine_year_month") }}', 'data-downloads'],
        provide_context=True,
    )

    extract_csv = PythonOperator(
        task_id='extract_csv',
        python_callable=extract_csv,
        op_args=['{{ task_instance.xcom_pull(task_ids="determine_year_month") }}', 'data-downloads'],
        provide_context=True,
    )

    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_args=['{{ task_instance.xcom_pull(task_ids="determine_year_month") }}', 'data-downloads'],
        provide_context=True,
    )

    upload_to_gcs_task = PythonOperator(
        task_id='upload_to_gcs',
        python_callable=upload_to_gcs,
        op_args=[BUCKET_NAME, '{{ task_instance.xcom_pull(task_ids="determine_year_month") }}', 'data-downloads'],
        provide_context=True,
    )

    determine_year_month_task >> download_zip >> extract_csv >> transform_data_task >> upload_to_gcs_task
