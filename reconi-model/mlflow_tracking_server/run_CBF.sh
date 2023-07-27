export MLFLOW_TRACKING_URI=http://reconi-mlflow.kro.kr:30003

mlflow run CBF \
--env-manager local \
--experiment-name CBF
