# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1) base 스테이지: 공통 파일 복사 & 의존성 설치
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FROM python:3.10 AS base
WORKDIR /app

# 스크립트
COPY load_model.py main.py ./

# 모델 디렉터리 전체를 복사
COPY distilgpt2_model ./distilgpt2_model

RUN pip install --no-cache-dir torch transformers

ENTRYPOINT ["python", "main.py"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2) full 전용 스테이지: 전체 모델만 포함
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FROM base AS full

# 기본 모드: full
RUN rm distilgpt2_model/pytorch_model_part1.bin \
       distilgpt2_model/pytorch_model_part2.bin \
       distilgpt2_model/pytorch_model_part3.bin \
       distilgpt2_model/pytorch_model_part4.bin \
       distilgpt2_model/pytorch_model_part5.bin

CMD ["--mode", "full"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3) part1 전용 스테이지: part1 모델만 포함
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FROM base AS part1

# 필요 없는 shard 삭제, part1만 pytorch_model.bin으로 이름 변경
RUN rm distilgpt2_model/pytorch_model.bin \
       distilgpt2_model/pytorch_model_part2.bin \
       distilgpt2_model/pytorch_model_part3.bin \
       distilgpt2_model/pytorch_model_part4.bin \
       distilgpt2_model/pytorch_model_part5.bin

CMD ["--mode", "partial"]
