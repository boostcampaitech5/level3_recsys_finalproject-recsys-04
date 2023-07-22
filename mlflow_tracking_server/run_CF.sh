export MLFLOW_TRACKING_URI=http://reconi-mlflow.kro.kr:30003

# mlflow run CF -P model=AutoRec \
mlflow run CF -P model=EASE \
--env-manager local \
--experiment-name CF
