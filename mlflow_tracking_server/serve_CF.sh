## CF
mlflow models serve \
-m /opt/ml/Recommendation-Modeling/mlflow_tracking_server/mlruns/167504472290418597/f46ef3b633eb4dfbb312759fd40b2b0d/artifacts/AutoRec \
-p 30006 \
--env-manager local \
--host 0.0.0.0


### use model registry
# mlflow models serve \
# -m models:/test_sota/1 \
# -p 30004 \
# --env-manager local
