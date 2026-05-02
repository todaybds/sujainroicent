"""
PDF 분양정보 기반으로 광고소재 4개 새로 만들기 (기존 2개는 삭제 또는 그대로)
"""
import hmac, hashlib, base64, time, json, requests

CUSTOMER_ID = "2553973"
API_KEY = "0100000000c702d5195228f5a8beab47a4f7764f89bacdd13c238b0b5a1417de7837f15150"
SECRET_KEY = "AQAAAADHAtUZUij1qL6rR6T3dk+JwFv9rwXHelEXd+997wTIXg=="
BASE_URL = "https://api.searchad.naver.com"

ADGROUP_ID = "grp-a001-01-000000065998872"
SITE_URL = "https://sujainroicent.com"
EXISTING_AD_IDS = ["nad-a001-01-000000517170483", "nad-a001-01-000000517170484"]

# PDF 분석 기반 4가지 컨셉
ADS = [
    {  # 컨셉1: 입지+규모
        "headline": "인하대역 수자인 로이센트",
        "description": "빛나는 용현학익 최중심 1,199세대! 인하대역 도보권 84·101㎡ 분양안내",
    },
    {  # 컨셉2: 분양가+혜택
        "headline": "인하대역 수자인 로이센트",
        "description": "84㎡ 6억대 분양가상한제 미적용 이자후불제, 견본주택 방문예약 운영중",
    },
    {  # 컨셉3: 브랜드+시공
        "headline": "인하대역 수자인 로이센트",
        "description": "BS한양 시공 한양 수자인 브랜드, 인하대역세권 신축 청약일정/평면도 안내",
    },
    {  # 컨셉4: 입주+생활권
        "headline": "인하대역 수자인 로이센트",
        "description": "2029년 4월 입주, 인하대·홈플러스·CGV 도보권 84·101㎡ 평면도 확인",
    },
]


def sig(ts, m, uri):
    return base64.b64encode(hmac.new(SECRET_KEY.encode(), f"{ts}.{m}.{uri}".encode(), hashlib.sha256).digest()).decode()

def req(method, uri, body=None, params=None):
    ts = str(int(time.time() * 1000))
    h = {"X-Timestamp": ts, "X-API-KEY": API_KEY, "X-Customer": CUSTOMER_ID,
         "X-Signature": sig(ts, method, uri), "Content-Type": "application/json; charset=UTF-8"}
    url = BASE_URL + uri
    if method == "GET":
        r = requests.get(url, headers=h, params=params, timeout=30)
    elif method == "POST":
        r = requests.post(url, headers=h, json=body, params=params, timeout=30)
    elif method == "PUT":
        r = requests.put(url, headers=h, json=body, params=params, timeout=30)
    elif method == "DELETE":
        r = requests.delete(url, headers=h, params=params, timeout=30)
    print(f"[{method}] {uri} -> HTTP {r.status_code}")
    if r.status_code not in (200, 201, 204):
        print(f"  ERR: {r.text[:600]}")
        return None
    if r.text:
        try: return r.json()
        except: return r.text
    return True


# 1. 기존 2개 광고소재 삭제
print("="*70); print("STEP 1. 기존 광고소재 2개 삭제 (간단 카피)"); print("="*70)
for ad_id in EXISTING_AD_IDS:
    req("DELETE", f"/ncc/ads/{ad_id}")

# 2. 새 4개 광고소재 생성
print()
print("="*70); print(f"STEP 2. 새 광고소재 {len(ADS)}개 생성 (PDF 기반)"); print("="*70)
final_url = f"{SITE_URL}/?utm_source=naver&utm_medium=sa&utm_campaign=sujain_roicent&utm_term={{keyword}}&utm_content={{adgroup_id}}"
for i, a in enumerate(ADS, 1):
    body = {
        "nccAdgroupId": ADGROUP_ID,
        "customerId": int(CUSTOMER_ID),
        "type": "TEXT_45",
        "ad": {
            "headline": a["headline"],
            "description": a["description"],
            "pc": {"display": SITE_URL, "final": final_url},
            "mobile": {"display": SITE_URL, "final": final_url},
        },
        "adAttr": {},
        "userLock": False,
    }
    r = req("POST", "/ncc/ads", body=body)
    if r:
        print(f"  ✅ #{i}: {r['nccAdId']}  '{a['description'][:30]}...'")
