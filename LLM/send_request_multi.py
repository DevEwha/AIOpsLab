# send_request_multi.py
import threading
import time
import requests

# 요청을 보낼 엔드포인트 URL (포트포워딩을 이미 켜 둔 상태여야 합니다)
URL = "http://localhost:8000/predict"

# 요청 페이로드 (FastAPI가 {"prompt": "..."} 형태를 처리하도록 구현되어 있어야 합니다)
PAYLOAD = {"prompt": "멀티 파드 테스트입니다."}

# 동시에 보낼 총 요청 개수
TOTAL_REQUESTS = 10

# 한 요청이 완료된 시점과 응답 시간을 기록하기 위한 저장소
results = []


def send_single_request(index: int):
    """
    index: 요청 번호 (디버깅용)
    """
    t0 = time.time()
    try:
        resp = requests.post(URL, json=PAYLOAD, timeout=30)
        t1 = time.time()
        latency = t1 - t0
        status = resp.status_code
        body = resp.json() if resp.headers.get("Content-Type", "").startswith("application/json") else resp.text
    except Exception as e:
        t1 = time.time()
        latency = t1 - t0
        status = None
        body = f"ERROR: {e}"

    # 결과를 전역 리스트에 저장
    results.append({
        "index": index,
        "status": status,
        "latency": latency,
        "body": body
    })


def main():
    threads = []

    print(f"[INFO] 총 {TOTAL_REQUESTS}개의 요청을 동시에 보냅니다.")
    t_start = time.time()

    # TOTAL_REQUESTS만큼 스레드를 생성하고 동시에 시작
    for i in range(TOTAL_REQUESTS):
        th = threading.Thread(target=send_single_request, args=(i,))
        threads.append(th)
        th.start()

    # 모든 스레드가 끝날 때까지 대기
    for th in threads:
        th.join()

    t_end = time.time()
    total_time = t_end - t_start

    # 결과 정리
    success_count = sum(1 for r in results if r["status"] == 200)
    error_count = TOTAL_REQUESTS - success_count

    print(f"\n[RESULT] 전체 소요 시간: {total_time:.2f}초")
    print(f"         성공 응답: {success_count}개, 실패/오류: {error_count}개\n")

    # 각 요청별 응답 상태와 지연 시간 출력
    for r in sorted(results, key=lambda x: x["index"]):
        print(f"  [{r['index']:02d}] 상태코드: {r['status']}, 지연: {r['latency']:.2f}초")

    # (선택) 상세 응답 바디 확인
    # for r in results:
    #     print(f"--- 요청 #{r['index']} 응답 바디 ---\n{r['body']}\n")


if __name__ == "__main__":
    main()
