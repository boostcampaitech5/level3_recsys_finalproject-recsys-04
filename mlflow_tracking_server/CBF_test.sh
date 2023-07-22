### CBF
# cold-start (user id 가 기존 데이터 (user_profile) 에 없어도 들고와져야합니다..!)
curl http://reconi-mlflow.kro.kr:30004/invocations \
-H 'Content-Type: application/json' \
--data '{
    "dataframe_records": [{"user_id":"이*혁", "Cupping Note 향미":7, "Cupping Note 산미":9, "Cupping Note 단맛":4, "Cupping Note 바디감":1, "Roasting Point":4.5}]
}'



# cold-start 아닐 때
# curl http://reconi-mlflow.kro.kr:30004/invocations \
# -H 'Content-Type: application/json' \
# --data '{"input":[베트남로부스타블루드래곤워시드g1, 마일드블렌드]}'


