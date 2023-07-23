mlflow models serve \
-m models:/CBF_1st_deploy/1 \
-p 30004 \
--env-manager local \
--host 0.0.0.0