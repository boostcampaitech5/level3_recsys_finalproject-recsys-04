### CF
curl http://reconi-mlflow.kro.kr:30004/invocations \
-H 'Content-Type: application/json' \
--data '{
    "dataframe_records": [{"user":"칸나꽃", "item":"아일리쉬향커피", "rating":2}, {"user":"댕댕아놀자", "item":"아일리쉬향커피", "rating":1}]
}'
