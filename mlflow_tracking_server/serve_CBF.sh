## CBF
mlflow models serve \
-m /opt/ml/Recommendation-Modeling/mlflow_tracking_server/mlruns/612821291203493459/39c5119cc86a4d5fbaa2795822bb6a20/artifacts/CBF \
-p 30004 \
--env-manager local \
--host 0.0.0.0