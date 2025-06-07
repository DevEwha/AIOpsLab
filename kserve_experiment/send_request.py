# send_request_timing.py
import time
import requests

def main():
    url = "http://localhost:8000/predict"
    payload = {"prompt": "Hello, world!"}

    try:
        t0 = time.time()
        resp = requests.post(url, json=payload, timeout=1000)
        t1 = time.time()

        latency = t1 - t0  # 초 단위 응답 시간
        print(f"Status Code: {resp.status_code}")
        print(f"Response Body: {resp.json()}")
        print(f"응답 시간: {latency:.3f}초")

    except requests.exceptions.RequestException as e:
        print("요청 중 예외 발생:", e)


if __name__ == "__main__":
    main()
