"""인하대 비즈채널 ID 조회 (검수 상태 확인용)"""
import hmac, hashlib, base64, time, json, requests

CUSTOMER_ID = "2553973"
API_KEY = "0100000000c702d5195228f5a8beab47a4f7764f89bacdd13c238b0b5a1417de7837f15150"
SECRET_KEY = "AQAAAADHAtUZUij1qL6rR6T3dk+JwFv9rwXHelEXd+997wTIXg=="
BASE_URL = "https://api.searchad.naver.com"

def sig(ts, m, uri):
    msg = f"{ts}.{m}.{uri}"
    s = hmac.new(SECRET_KEY.encode(), msg.encode(), hashlib.sha256)
    return base64.b64encode(s.digest()).decode()

def req(method, uri, params=None):
    ts = str(int(time.time()*1000))
    h = {
        "X-Timestamp": ts, "X-API-KEY": API_KEY, "X-Customer": CUSTOMER_ID,
        "X-Signature": sig(ts, method, uri),
        "Content-Type": "application/json; charset=UTF-8",
    }
    url = BASE_URL + uri
    if method == "GET":
        r = requests.get(url, headers=h, params=params, timeout=30)
    else:
        r = requests.post(url, headers=h, json=params, timeout=30)
    print(f"[{method}] {uri} -> HTTP {r.status_code}")
    if r.status_code != 200:
        print("  ERR:", r.text[:500])
        return None
    try: return r.json()
    except: return r.text

print("="*70); print("[1] 캠페인 목록"); print("="*70)
cs = req("GET", "/ncc/campaigns")
if cs:
    for c in cs:
        print(f"  {c.get('nccCampaignId')}  '{c.get('name')}'  channelId={c.get('nccBusinessChannelId') or c.get('channelId')}  status={c.get('status')}")

print()
print("="*70); print("[2] 캠페인 디테일 (nccChannelId 확인용)"); print("="*70)
if cs:
    sample = cs[2]['nccCampaignId']  # 칸타빌
    d = req("GET", f"/ncc/campaigns/{sample}")
    if d:
        print(json.dumps(d, ensure_ascii=False, indent=2)[:1500])

print()
print("="*70); print("[3] channels 후보 endpoint"); print("="*70)
for path in ["/ncc/channels", "/ncc/biz-channel", "/ncc/biz-channels"]:
    r = req("GET", path)
    if r and isinstance(r, list):
        print(f"  found! {len(r)} items")
        for ch in r:
            print(" ", ch)
