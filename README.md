# Introduction
커피 플레이리스트(커플) 서비스에 사용된 추천시스템 모델 repository 입니다.

## Cold-start
### User survey 결과와 아이템 간 유사도를 계산하여 추천
<img width="647" alt="notCold-1" src="https://github.com/RecoRecoNi/Recommendation-Modeling/assets/86715604/07c91420-f7e0-437c-9e1a-1ea0b4abf79e">


## Not cold-start
### STEP 1 : 아이템의 description 컬럼으로부터 키워드 추출 및 전체 아이템에 대한 코사인 유사도 계산 (pre-step)
<img width="720" alt="notCold-2" src="https://github.com/RecoRecoNi/Recommendation-Modeling/assets/86715604/5b329f2c-6229-4510-b89e-f48c3f66954e">

### STEP 2 : 유저가 상호작용한 아이템들로부터 CBF 를 통해 유사한 아이템 - 기존 상호작용이 존재하는 특정 로스터리의 아이템을 추출
<img width="904" alt="notCold-3" src="https://github.com/RecoRecoNi/Recommendation-Modeling/assets/86715604/7eca612d-01bd-4006-8270-c85d28c3c2f4">

### STEP 3 : 이전에 필터링한 특정 로스터리의 아이템을 CF 모델의 입력으로 넣은 뒤, 추천된 아이템과 유사한 아이템을 특정 로스터리 이외에서 CBF 로 추천
<img width="788" alt="Cold" src="https://github.com/RecoRecoNi/Recommendation-Modeling/assets/86715604/8b7b97bf-6e37-4eb0-979a-fa3d281652bb">

# Prerequsites

```bash
poetry install # when initial run
poetry shell

cd mlflow_tracking_server
```

# How to run?
## For tracking/training
### baseline (release-v1)

- cold-start (O)
    ```bash
    sh run_CBF.sh
    ```

- cold-start (X)
    ```bash
    sh run_CF.sh
    ```

### experiment (custom)

- cold-start (O)
    ```bash
    mlflow run CBF \
    --env-manager local \
    --experiment-name CBF

    """
    여러 실험을 통해 최종적으로 선택할 모델을 mlflow gui 상에서 registry 에 등록합니다.
    """
    ```

- cold-start (X)
    ```bash
    """
    새로운 실험을 위해 원하는 모델의 yaml 하이퍼파라미터를 수정합니다.
    """
    
    mlflow run CF -P model={yaml 에 존재하는 모델} -P config_name={yaml 에 존재하는 config_name} \
    --env-manager local \
    --experiment-name CF

    """
    여러 실험을 통해 최종적으로 선택할 모델을 mlflow gui 상에서 registry 에 등록합니다.
    """
    ```

## For serving
### baseline (release-v1)

- cold-start (O)
    ```bash
    sh serve_CBF.sh
    ```

- cold-start (X)
    ```bash
    sh serve_CF.sh
    ```

### experiment (custom)

- cold-start (O)
    ```bash
    mlflow models serve \
    -m models:/{mlflow registery 에 등록된 모델 이름}/{mlflow registry 에 등록된 버전} \
    -p 30004 \
    --env-manager local \
    --host 0.0.0.0
    ```

- cold-start (X)
    ```bash
    mlflow models serve \
    -m models:/{mlflow registery 에 등록된 모델 이름}/{mlflow registry 에 등록된 버전} \
    -p 30005 \
    --env-manager local \
    --host 0.0.0.0
    ```
