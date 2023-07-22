### CBF
# cold-start : output -> {"predictions": [232, 311, 82, 273, 156]}
# curl http://reconi-mlflow.kro.kr:30004/invocations \
# -H 'Content-Type: application/json' \
# --data '{
#     "dataframe_records": [{"aroma":7, "acidity":9, "sweetness":4, "body_feel":1, "roasting_characteristics":4.5}]
# }'


# # not cold-start : output -> {"predictions": [72, 99]}
curl http://reconi-mlflow.kro.kr:30005/invocations \
-H 'Content-Type: application/json' \
--data '{"inputs": [3, 5]}' # 콩스콩스 아이템 전체