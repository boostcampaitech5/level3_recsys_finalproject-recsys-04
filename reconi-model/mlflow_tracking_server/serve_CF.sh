mlflow models serve \
-m models:/CF_2nd_deploy/1 \
-p 30005 \
--env-manager local \
--host 0.0.0.0