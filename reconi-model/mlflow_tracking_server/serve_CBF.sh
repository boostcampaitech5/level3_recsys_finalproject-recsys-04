mlflow models serve \
-m models:/CBF_2nd_deploy/1 \
-p 30004 \
--env-manager local \
--host 0.0.0.0