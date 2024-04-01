from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount

default_args = {
'owner'                 : 'airflow',
'description'           : 'Use of the DockerOperator',
'start_date'            : datetime(2021, 5, 1),
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

with DAG('dbt_run_project', default_args=default_args, schedule_interval=timedelta(minutes=5), catchup=False) as dag:

    t1 = BashOperator(
        task_id='print_current_date',
        bash_command='date'
        )
        
    t2 = DockerOperator(
        task_id='docker_command_sleep',
        image='dbt-bigquery:v1',
        container_name='docker-proxy-run',
        api_version='auto',
        auto_remove=True,
        #command="bash -c 'dbt build'",
        command="run --project-dir /usr/app/dbt/capital_bikeshare",
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        mounts = [
            Mount(source="/dbt/projects", target="/usr/app", type="bind"),
            Mount(source="/dbt/config",target="/root/.dbt",type="bind")
            ],
        mount_tmp_dir = False
        )

    t3 = BashOperator(
        task_id='end_task',
        bash_command='echo "Task finished succesfully"'
        )

    t1 >> t2 >> t3