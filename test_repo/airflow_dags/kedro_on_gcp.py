from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import  DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator

default_args = {
    'depends_on_past': False   
}

CLUSTER_NAME = 'airflow-cluster'
REGION='us-central1'
PROJECT_ID='bionic-spot-337303'
PYSPARK_URI='gs://demo_scripts/pyspark_demo.py'   


CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n1-standard-2",
        "disk_config": {"boot_disk_type": "pd-standard", "boot_disk_size_gb": 500,"num_local_ssds":0},
    },
    "software_config":{
    "image_version":"2.0-debian10",
    "properties":{"dataproc:dataproc.allow.zero.workers": "true"}
   
} ,"initialization_actions":[{
  "executable_file": "gs://us-central1-airflow-9a7d7fdd-bucket/dags/install.sh"
}]
}

PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {"main_python_file_uri": PYSPARK_URI},
}

with DAG(
    'kedro-on-gcp',
    default_args=default_args,
    description='A simple DAG to create a Dataproc workflow',
    schedule_interval=None,
    start_date = days_ago(2)
) as dag:

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=REGION,
        cluster_name=CLUSTER_NAME,
    )

    submit_job = DataprocSubmitJobOperator(
        task_id="pyspark_task", 
        job=PYSPARK_JOB, 
        location=REGION, 
        project_id=PROJECT_ID
    )

    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster", 
        project_id=PROJECT_ID, 
        cluster_name=CLUSTER_NAME, 
        region=REGION
    )


    create_cluster >> submit_job >> delete_cluster
