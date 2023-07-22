## CBF
# cold-start (X)
mlflow models serve \
-m /opt/ml/Recommendation-Modeling/mlflow_tracking_server/mlruns/612821291203493459/94f4c5e730874f1d809a71ec55227523/artifacts/CBF \
-p 30005 \
--env-manager local \
--host 0.0.0.0