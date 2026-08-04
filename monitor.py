import hashlib
import os
import requests

URL = "https://cp.toyota.jp/rentacar/"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

DATA_FILE = "last_hash.txt"

html = requests.get(URL, timeout=30).text
current_hash = hashlib.sha256(html.encode()).hexdigest()

old_hash = None
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        old_hash = f.read().strip()

if old_hash is None:
    print("初回実行")
elif old_hash != current_hash:
    requests.post(
        WEBHOOK,
        json={
            "content": f"🚨 トヨタレンタカーのページが更新されました！\n{URL}"
        },
        timeout=30,
    )
    print("通知しました")
else:
    print("変更なし")

with open(DATA_FILE, "w") as f:
    f.write(current_hash)
