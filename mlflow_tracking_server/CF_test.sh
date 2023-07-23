curl http://reconi-mlflow.kro.kr:30005/invocations \
-H 'Content-Type: application/json' \
--data '{
    "dataframe_records": [{"user":"1", "item":1, "rating":1}, {"user":"1", "item":0, "rating":1}, {"user":"1", "item":2, "rating":1}, {"user":"1", "item":3, "rating":1}]
}'