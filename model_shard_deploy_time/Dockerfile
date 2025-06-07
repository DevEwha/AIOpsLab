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

# part shard 파일 모두 제거
RUN rm -f distilgpt2_model/pytorch_model_part*.bin

CMD ["--mode", "full"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3) part1 전용 스테이지: part1 모델만 포함
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FROM base AS part1

# 원본 모델 파일과 다른 shards 제거, part1 shard는 그대로 유지
RUN rm -f distilgpt2_model/pytorch_model.bin && \
    for f in distilgpt2_model/pytorch_model_part*.bin; do \
      [ "$f" != "distilgpt2_model/pytorch_model_part1.bin" ] && rm -f "$f"; \
    done

CMD ["--mode", "partial"]
