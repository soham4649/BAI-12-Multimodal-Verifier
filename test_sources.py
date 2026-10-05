import requests
import time

url = "http://127.0.0.1:5000/verify"
img_path = r"C:\Users\admin\Downloads\tata_punch_real.jpg"
claim = "this image shows a BMW car"

t0 = time.time()
res = requests.post(url, files={"image": open(img_path, "rb")}, data={"claim": claim}).json()
dt = time.time() - t0

ev = res.get("evidence", [])
print(f"Status: {res.get('status')}")
print(f"Result: {res.get('result')}")
print(f"Combined Score: {res.get('combined_score')}%")
print(f"Sources count: {len(ev)}")
print(f"Total Time: {dt:.2f}s")

print("\nReturned Sources:")
for i, s in enumerate(ev, 1):
    print(f"  {i}. [{s.get('domain')}] {s.get('title')}")
    print(f"     Link: {s.get('link')}")
    print(f"     Snippet: {s.get('snippet')[:90]}...")
