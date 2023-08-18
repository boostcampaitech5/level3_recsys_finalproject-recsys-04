export MLFLOW_TRACKING_URI=http://reconi-mlflow.kro.kr:30003

mlflow run CF -P model=EASE -P config_name=ver06 \
--env-manager local \
--experiment-name CF
