# Model
커피 플레이리스트(커플) 서비스에 사용된 추천시스템 모델 repository 입니다.

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