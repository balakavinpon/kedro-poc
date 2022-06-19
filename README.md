# kedro-poc

# On Your Cloud Shell:

PROJECT_ID=kedro-kubeflow-334417

REGION=us-central1

gcloud config set project $PROJECT_ID

## To checkout the code and install dependencies

git clone https://github.com/balakavinpon/kedro-poc.git --branch kfp

pip install virtualenv

virtualenv venv-kedro

source venv-kedro/bin/activate

cd kedro-poc/test-repo
pip install -r src/requirements.txt 

export KEDRO_CONFIG_RUN_ID="234"

export KEDRO_GLOBALS_PATTERN="*globals.yml"

## To build the docker image 

kedro docker build

docker images

## To push the docker image to container registry 

docker tag test_repo:latest   gcr.io/$PROJECT_ID/test_repo:latest

docker push   gcr.io/$PROJECT_ID/test_repo:latest


## To verify the code before running on Vertex AI:

kedro docker run --image "gcr.io/$PROJECT_ID/test_repo:latest"


## To run the code on Vertex AI 

vi conf/base/kubeflow.yaml 
modify line number # 4 , 5 and 11 with ProjectId, region and full docker image URL. 

export SERVICE_ACCOUNT="service account to run KFP job"

kedro kubeflow run-once 
