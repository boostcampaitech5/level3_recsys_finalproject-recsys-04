curl http://reconi-mlflow.kro.kr:30004/invocations \
-H 'Content-Type: application/json' \
--data '{
    "dataframe_records": [{"aroma":7, "acidity":9, "sweetness":4, "body_feel":1, "roasting_characteristics":4.5}]
}'