echo "This is the start of execution"
PWD=`pwd`
echo $PWD
gsutil cp -r gs://kedro-kubeflow-334417-code-staging/kedro-poc $PWD
ls -l $PWD

ls -l $PWD/kedro-poc/test_repo

pip install -r $PWD/kedro-poc/test_repo/src/requirements.txt
