from collections import defaultdict

from pathlib import Path

from airflow import DAG
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.version import version
from datetime import datetime, timedelta

from kedro.framework.session import KedroSession
from kedro.framework.project import configure_project


class KedroOperator(BaseOperator):

    @apply_defaults
    def __init__(
        self,
        package_name: str,
        pipeline_name: str,
        node_name: str,
        project_path: str,
        env: str,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.package_name = package_name
        self.pipeline_name = pipeline_name
        self.node_name = node_name
        self.project_path = project_path
        self.env = env

    def execute(self, context):
        configure_project(self.package_name)
        with KedroSession.create(self.package_name,
                                 self.project_path,
                                 env=self.env) as session:
            session.run(self.pipeline_name, node_names=[self.node_name])

# Kedro settings required to run your pipeline
env = "local"
pipeline_name = "__default__"
project_path = Path.cwd()
package_name = "pkg"

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(
    "pkg",
    start_date=datetime(2019, 1, 1),
    max_active_runs=3,
    schedule_interval=timedelta(minutes=30),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    default_args=default_args,
    catchup=False # enable if you don't want historical dag runs to run
) as dag:

    tasks = {}

    tasks["data-acquisition-parameters-dataset"] = KedroOperator(
        task_id="data-acquisition-parameters-dataset",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="data_acquisition([parameters]) -> [dataset]",
        project_path=project_path,
        env=env,
    )

    tasks["feature-engineering-dataset-parameters-cleaned-dataset"] = KedroOperator(
        task_id="feature-engineering-dataset-parameters-cleaned-dataset",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="feature_engineering([dataset,parameters]) -> [cleaned_dataset]",
        project_path=project_path,
        env=env,
    )

    tasks["train-test-split-fun-cleaned-dataset-parameters-x-test-x-train-y-test-y-train"] = KedroOperator(
        task_id="train-test-split-fun-cleaned-dataset-parameters-x-test-x-train-y-test-y-train",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="train_test_split_fun([cleaned_dataset,parameters]) -> [x_test,x_train,y_test,y_train]",
        project_path=project_path,
        env=env,
    )

    tasks["model-training-parameters-x-train-y-train-model"] = KedroOperator(
        task_id="model-training-parameters-x-train-y-train-model",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="model_training([parameters,x_train,y_train]) -> [model]",
        project_path=project_path,
        env=env,
    )

    tasks["validation-model-parameters-x-test-y-test-metrics"] = KedroOperator(
        task_id="validation-model-parameters-x-test-y-test-metrics",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="validation([model,parameters,x_test,y_test]) -> [metrics]",
        project_path=project_path,
        env=env,
    )



    tasks["train-test-split-fun-cleaned-dataset-parameters-x-test-x-train-y-test-y-train"] >> tasks["model-training-parameters-x-train-y-train-model"]

    tasks["train-test-split-fun-cleaned-dataset-parameters-x-test-x-train-y-test-y-train"] >> tasks["validation-model-parameters-x-test-y-test-metrics"]

    tasks["model-training-parameters-x-train-y-train-model"] >> tasks["validation-model-parameters-x-test-y-test-metrics"]

    tasks["data-acquisition-parameters-dataset"] >> tasks["feature-engineering-dataset-parameters-cleaned-dataset"]

    tasks["feature-engineering-dataset-parameters-cleaned-dataset"] >> tasks["train-test-split-fun-cleaned-dataset-parameters-x-test-x-train-y-test-y-train"]
