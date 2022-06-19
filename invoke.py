import base64
import json
from google.cloud import aiplatform

PROJECT_ID = 'dataproc-serverless-351706'                     # <---CHANGE THIS
REGION = 'us-east4'                             # <---CHANGE THIS
PIPELINE_ROOT = 'gs://dataproc-serverless-351706-kedro-poc/' # <---CHANGE THIS

def subscribe(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    print("Kedro-run-CF invoked")
    # decode the event payload string
    payload_message = base64.b64decode(event['data']).decode('utf-8')
    print("payload->",payload_message)
    # parse payload string into JSON object
    payload_json = json.loads(payload_message)
    # trigger pipeline run with payload
    trigger_pipeline_run(payload_json)

def trigger_pipeline_run(payload_json):
    """Triggers a pipeline run
    Args:
        payload_json: expected in the following format:
            {
            "pipeline_spec_uri": "<path-to-your-compiled-pipeline>",
            "parameter_values": {
                "greet_name": "<any-greet-string>"
            }
            }
    """
    pipeline_spec_uri = payload_json['pipeline_spec_uri']
    parameter_values = payload_json['parameter_values']

    print("URI->",pipeline_spec_uri)

    # Create a PipelineJob using the compiled pipeline from pipeline_spec_uri
    aiplatform.init(
        project=PROJECT_ID,
        location=REGION,
    )
    job = aiplatform.PipelineJob(
        display_name='kedro-repo-cloud-function-invocation',
        template_path=pipeline_spec_uri,
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
        parameter_values=parameter_values
    )

    # Submit the PipelineJob
    job.submit()

if __name__=="__main__":
    payload_message="""
{
    "pipeline_spec_uri": "gs://dataproc-serverless-351706-kedro-poc/pipeline/pipe.json",
    "parameter_values": {
    }
}
    """
    print("payload->",payload_message)
    # parse payload string into JSON object
    payload_json = json.loads(payload_message)
    # trigger pipeline run with payload
    trigger_pipeline_run(payload_json)