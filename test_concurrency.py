import requests
import threading

URL = "http://127.0.0.1:8000/api/agent/query"

payload = {
    "message": "create github issue concurrency test"
}

def make_request(i):
    try:
        response = requests.post(URL, json=payload)
        print(f"Request {i}: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Request {i} failed: {e}")

threads = []

for i in range(5):
    t = threading.Thread(target=make_request, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()