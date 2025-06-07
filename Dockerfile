# Dockerfile
FROM python:3.9

# 필수 라이브러리와 함께 PyTorch를 설치하도록 수정
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    transformers \
    torch

COPY app.py /app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
