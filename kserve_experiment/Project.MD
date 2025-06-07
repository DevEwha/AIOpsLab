## 📂 폴더 구조

```plaintext
llm-kserve-experiment/
├── app.py                 # FastAPI 애플리케이션 엔트리포인트
├── inference.yaml         # KServe InferenceService 설정 파일
├── send_request.py        # 클라이언트 테스트용 스크립트
├── requirements.txt       # Python 의존성 목록
├── Dockerfile             # 컨테이너 이미지 빌드를 위한 도커파일
└── README.md              # 프로젝트 설명서
```

## 🚀 프로젝트 개요

이 프로젝트는 Hugging Face의 `distilgpt2` 모델을 KServe를 통해 서버리스 방식으로 배포하고, 로컬에서 port-forward를 사용해 테스트하는 예제입니다.

## 🔧 사전 준비

1. **Kubernetes 클러스터** (예: Kind, Minikube) 설치 및 준비
2. **KServe** 설치 및 설정 완료
3. **kubectl** 명령어 사용 가능
4. 로컬에 **Python 3.8+** 설치
5. (선택) Docker 및 컨테이너 레지스트리 접근 권한

## ⚙️ 설치 및 실행

1. 의존성 설치

   ```bash
   cd llm-kserve-experiment
   pip install -r requirements.txt
   ```

2. 컨테이너 이미지 빌드 & 푸시

   ```bash
   docker build -t <your-registry>/llm-server:latest .
   docker push <your-registry>/llm-server:latest
   ```

3. `inference.yaml` 에 이미지 경로 업데이트

   ```yaml
   spec:
     predictor:
       containers:
       - image: <your-registry>/llm-server:latest
         name: llm-container
   ```

4. InferenceService 생성

   ```bash
   kubectl apply -f inference.yaml -n kserve
   ```

5. 서비스 상태 확인

   ```bash
   kubectl get inferenceservice llm-server -n kserve
   ```

6. Port-forward 실행 (다른 터미널에서)

   ```bash
   kubectl port-forward svc/llm-server-predictor-00001 8000:80 -n kserve
   ```

7. 로컬 테스트

   * **curl**

     ```bash
     curl -X POST http://localhost:8000/predict \
       -H "Content-Type: application/json" \
       -d '{"prompt":"Hello, world!"}'
     ```
   * **send\_request.py**

     ```bash
     python send_request.py
     ```

## 📄 파일 설명

* **app.py**: FastAPI 기반 서버 코드. 모델 로드 및 `/predict` 엔드포인트 구현.
* **inference.yaml**: KServe InferenceService CRD. 모델 이미지, 리소스 설정 포함.
* **send\_request.py**: `requests` 라이브러리를 이용해 로컬 엔드포인트에 테스트 요청을 보내고 결과 출력.
* **requirements.txt**: `fastapi`, `uvicorn`, `transformers`, `requests` 등 필요 패키지 목록.
* **Dockerfile**: FastAPI 앱을 컨테이너화하기 위한 설정.

## 🛠️ 자주 발생하는 문제

* **Port-forward 연결 실패**: 서비스 이름(`svc/llm-server-predictor-00001`)과 네임스페이스(`kserve`) 확인
* **Read timed out**: 클라이언트 `timeout` 값 조정 또는 모델 로딩 시간 확인
* **Pod 미생성**: `kubectl describe inferenceservice llm-server -n kserve` 로 이벤트 확인

## 📚 참고

* [KServe 공식 문서](https://kserve.github.io/)