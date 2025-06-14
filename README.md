# Serverless LLM Cold Start Research 

## 📂 전체 디렉토리 구조

```plaintext
🗂️
├── Project.MD               # 연구 개요, 배경, 평가 지표, 일정 등 전반적 계획서
├── GroundRule.MD            # 팀 협업 규칙, PR 승인 절차, 커밋 메시지 가이드
├── kserve_experiment/       # KServe 기반 실험 환경
│   ├── Dockerfile           # 컨테이너 이미지 빌드 설정 (quantization/pruning 포함)
│   ├── app.py               # FastAPI 서버 코드
│   ├── inference.yaml       # KServe InferenceService CRD 설정
│   ├── send_request.py      # 첫 요청 및 연속 요청 지연 시간 측정 스크립트
│   ├── requirements.txt     # Python 의존성 목록
│   └── Project.md           # 해당 실험 폴더 전용 가이드
├── model_shard_deploy_time/ # CPU 환경 분할 로딩을 통한 콜드 스타트 완화 실험
│   ├── distilgpt2_model/    # 분할 전 모델 및 config, tokenizer, 분할 후 모델
│   ├── load_model.py        # 모델 다운로드 및 state_dict 저장 스크립트
│   ├── divide_model.py      # CPU 기반 모델 weight 분할 스크립트
│   ├── main.py              # 전체 vs. 파셜 로드 시간 측정 스크립트
│   └── Dockerfile           # Multi-stage 컨테이너 이미지 정의
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
* **model\_shard_deploy\_time/**: CPU 환경 분할 로딩을 통한 콜드 스타트 완화 실험

## 🛠️ 실험1) CPU 환경 분할 로딩을 통한 콜드 스타트 완화 실험(model\_shard_deploy\_time)
- GPU 사용이 어려운 환경에서도 모델을 여러 샤드(shard)로 분할 저장·로딩하여 초기 로드 시간을 단축하는 방식을 제안합니다.
- 기대 효과 및 결론
  - CPU 환경에서도 모델 로딩 초기화 시간(cold start)을 유의미하게 단축
  - GPU 환경에서는 디바이스 초기화, I/O 병목 완화 효과가 더 크게 나타날 것으로 기대
  - 모델 크기 증가 시 샤딩 효과(+초기화 단축 비율)가 더욱 증폭
  - 결과적으로 “모델을 여러 인스턴스에 나눠 저장·로드하는 협업 추론 구조”는 서버리스·컨테이너 확장 시 빠른 스케일 아웃을 지원
- 자세한 내용 및 실행 방법은 [pr #2](https://github.com/DevEwha/AIOpsLab/pull/2) 참고

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
* MegatronLM HuggingFace: [https://huggingface.co/.../megatron_lm](https://huggingface.co/docs/accelerate/usage_guides/megatron_lm)

---

