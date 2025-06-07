# Serverless LLM Cold Start Research 

## 📂 전체 디렉토리 구조

```plaintext
├── Project.MD               # 연구 개요, 배경, 평가 지표, 일정 등 전반적 계획서
├── GroundRule.MD            # 팀 협업 규칙, PR 승인 절차, 커밋 메시지 가이드
├── kserve_experiment/       # KServe 기반 실험 환경
│   ├── Dockerfile           # 컨테이너 이미지 빌드 설정 (quantization/pruning 포함)
│   ├── app.py               # FastAPI 서버 코드
│   ├── inference.yaml       # KServe InferenceService CRD 설정
│   ├── send_request.py      # 첫 요청 및 연속 요청 지연 시간 측정 스크립트
│   ├── requirements.txt     # Python 의존성 목록
│   └── Project.md           # 해당 실험 폴더 전용 가이드
├── other_experiment/        # 추가 실험용 디렉토리 (예: Ray Serve, Lambda 백엔드 등)
│   └── README.md            # 각 실험별 가이드
└── README.md                # 이 파일: 연구 전체 안내서
```

## 🚀 연구 배경

* 최근 LLM을 서버리스 함수 또는 컨테이너 기반 인프라에 배포할 때, 첫 요청 시 모델 로딩 및 초기화로 인한 **콜드 스타트 지연**이 큰 문제로 대두
* 지연 시간은 사용자 경험과 비용 효율성에 직접적 영향을 미침

## 🎯 연구 목표

1. 서버리스 플랫폼(KServe, AWS Lambda 등)에서 **콜드 스타트 시간**을 정량적으로 측정
2. 다양한 **최적화 기법**(모델 분할, 지연 로딩, 이미지 경량화, collaborative inference 등)의 효과 비교
3. 실험 결과를 바탕으로 **Best Practice** 및 오픈소스 도구 개선안 제안

## 🗂️ 주요 구성

* **Project.MD**: 연구 동기, 문헌 리뷰, 실험 설계, 평가 지표, 일정 계획 등 전반 문서
* **GroundRule.MD**: 팀별 협업 규칙과 PR/CI 워크플로우, 코드 스타일 가이드
* **kserve\_experiment/**: KServe 기반 실험 환경 및 결과 재현 코드
* **other\_experiment/**: 추후 확장 가능한 다양한 서버리스 플랫폼 실험 디렉토리

## 🛠️ 실험2) kserve baseline (kserve\_experiment)

1. Docker 이미지 빌드 & 레지스트리 푸시
2. KServe InferenceService 배포 (`inference.yaml` 적용)
3. Port-Forward or Ingress 설정으로 로컬/외부 호출 환경 구성
4. `send_request.py`로 첫 요청과 예열(warm-up) 요청 지연 시간 측정
5. 로그/메트릭 수집 후 분석 스크립트 실행

자세한 단계는 `kserve_experiment/README.md` 참고

## 📚 참고 자료

* KServe Documentation: [https://kserve.github.io/](https://kserve.github.io/)
* FastAPI Documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

---

