## CF
mlflow models serve \
-m /opt/ml/Recommendation-Modeling/mlflow_tracking_server/mlruns/167504472290418597/b125af4d05fb404aae3737a2f0e7cde6/artifacts/AutoRec \
-p 30004 \
--env-manager local \
--host 0.0.0.0


### use model registry
# mlflow models serve \
# -m models:/test_sota/1 \
# -p 30004 \
# --env-manager local
