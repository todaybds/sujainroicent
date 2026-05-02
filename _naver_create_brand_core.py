"""
인하대역 수자인 로이센트 — 네이버 검색광고 캠페인 + '브랜드 핵심' 광고그룹 자동 생성

생성:
  1. 캠페인 1개 (status=PAUSED 시작 — 사용자가 검수 통과 후 ON)
  2. 광고그룹 1개 (브랜드 핵심, bid=8000)
  3. 광고소재 2개 (헤드라인+설명 다른 버전)
  4. 키워드 12개 (정식브랜드명만 5000원 override, 나머지 그룹값 사용)
"""
import hmac, hashlib, base64, time, json, requests, sys

# === 인증 ===
CUSTOMER_ID = "2553973"
API_KEY = "0100000000c702d5195228f5a8beab47a4f7764f89bacdd13c238b0b5a1417de7837f15150"
SECRET_KEY = "AQAAAADHAtUZUij1qL6rR6T3dk+JwFv9rwXHelEXd+997wTIXg=="
BASE_URL = "https://api.searchad.naver.com"

# === 인하대 ===
BIZCHANNEL_ID = "bsn-a001-00-000000014086536"
SITE_URL = "https://sujainroicent.com"
CAMPAIGN_NAME = "인하대역 수자인 로이센트"
ADGROUP_NAME = "인하대역 수자인 로이센트_브랜드 핵심"
ADGROUP_BID = 8000
UTM_CAMPAIGN = "sujain_roicent"

# === 광고소재 ===
ADS = [
    {"headline": "인하대역 수자인 로이센트",
     "description": "인하대 역세권 빛나는 최중심 단지! 84/101㎡ 분양안내 견본주택 방문예약"},
    {"headline": "인하대역 수자인 로이센트",
     "description": "인하대역 도보권 신축 아파트, 한양 수자인 브랜드 분양가/평면도 확인"},
]

# === 키워드 (정식명만 개별 5000원 override) ===
KEYWORDS = [
    ("인하대역수자인", None),
    ("인하대역수자인로이센트", 5000),
    ("수자인로이센트", None),
    ("인하대수자인", None),
    ("미추홀구수자인", None),
    ("용현동수자인로이센트", None),
    ("인하대역로이센트", None),
    ("한양수자인로이센트", None),
    ("BS한양수자인", None),
    ("수자인로이센트분양가", None),
    ("수자인로이센트모델하우스", None),
    ("수자인로이센트청약", None),
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
    if r.status_code not in (200, 201):
        print(f"  ERR: {r.text[:600]}")
        return None
    try: return r.json()
    except: return r.text


# ============================================================
# 1) 캠페인 — 이미 생성된 ID 재사용 (재실행 시 중복 방지)
# ============================================================
print("="*70); print("STEP 1. 캠페인 확인"); print("="*70)
CAMPAIGN_ID = "cmp-a001-01-000000010584028"
camp = req("GET", f"/ncc/campaigns/{CAMPAIGN_ID}")
if not camp:
    print("기존 캠페인 조회 실패. 새로 생성 시도...")
    campaign_body = {
        "customerId": int(CUSTOMER_ID),
        "name": CAMPAIGN_NAME,
        "campaignTp": "WEB_SITE",
        "deliveryMethod": "ACCELERATED",
        "trackingMode": "AUTO_TRACKING_MODE",
        "useDailyBudget": False, "dailyBudget": 0, "usePeriod": False,
    }
    camp = req("POST", "/ncc/campaigns", body=campaign_body)
    if not camp: sys.exit(1)
    CAMPAIGN_ID = camp["nccCampaignId"]
print(f"  ✅ 캠페인: {CAMPAIGN_ID}  '{camp['name']}'  status={camp.get('status')}")

# ============================================================
# 2) 광고그룹 생성
# ============================================================
print()
print("="*70); print("STEP 2. 광고그룹 생성 (브랜드 핵심)"); print("="*70)
adgroup_body = {
    "customerId": int(CUSTOMER_ID),
    "nccCampaignId": CAMPAIGN_ID,
    "name": ADGROUP_NAME,
    "adgroupType": "WEB_SITE",
    "adgroupAttrJson": {"campaignTp": 1},
    "pcChannelId": BIZCHANNEL_ID,
    "mobileChannelId": BIZCHANNEL_ID,
    "bidAmt": ADGROUP_BID,
    "useDailyBudget": False,
    "dailyBudget": 0,
    "useCntsNetworkBidAmt": False,
    "contentsNetworkBidAmt": 70,
    "mobileNetworkBidWeight": 100,
    "pcNetworkBidWeight": 100,
    "userLock": False,
    "targets": [
        {"targetTp": "PC_MOBILE_TARGET", "target": {"pc": True, "mobile": True}},
    ],
}
ag = req("POST", "/ncc/adgroups", body=adgroup_body)
if not ag:
    print("광고그룹 생성 실패. 중단.")
    sys.exit(1)
ADGROUP_ID = ag["nccAdgroupId"]
print(f"  ✅ 생성: {ADGROUP_ID}  '{ag['name']}'  bid={ag['bidAmt']}")

# ============================================================
# 3) 광고소재 생성 (2개)
# ============================================================
print()
print("="*70); print(f"STEP 3. 광고소재 {len(ADS)}개 생성"); print("="*70)
final_url_tpl = f"{SITE_URL}/?utm_source=naver&utm_medium=sa&utm_campaign={UTM_CAMPAIGN}&utm_term={{keyword}}&utm_content={{adgroup_id}}"
created_ad_ids = []
for ad in ADS:
    ad_body = {
        "nccAdgroupId": ADGROUP_ID,
        "customerId": int(CUSTOMER_ID),
        "type": "TEXT_45",
        "ad": {
            "headline": ad["headline"],
            "description": ad["description"],
            "pc": {"display": SITE_URL, "final": final_url_tpl},
            "mobile": {"display": SITE_URL, "final": final_url_tpl},
        },
        "adAttr": {},
        "userLock": False,
    }
    a = req("POST", "/ncc/ads", body=ad_body)
    if a:
        created_ad_ids.append(a["nccAdId"])
        print(f"  ✅ 생성: {a['nccAdId']}  inspect={a.get('inspectStatus')}")

# ============================================================
# 4) 키워드 등록 (배치)
# ============================================================
print()
print("="*70); print(f"STEP 4. 키워드 {len(KEYWORDS)}개 등록"); print("="*70)
kw_list = []
for kw, bid in KEYWORDS:
    if bid is None:
        kw_list.append({"keyword": kw, "useGroupBidAmt": True})
    else:
        kw_list.append({"keyword": kw, "useGroupBidAmt": False, "bidAmt": bid})

kw_resp = req("POST", "/ncc/keywords", body=kw_list, params={"nccAdgroupId": ADGROUP_ID})
if kw_resp:
    print(f"  ✅ 등록 {len(kw_resp)}개")
    for k in kw_resp:
        print(f"    {k.get('nccKeywordId')}  '{k.get('keyword')}'  bid={k.get('bidAmt')}  useGrp={k.get('useGroupBidAmt')}  status={k.get('status')}")

# ============================================================
# 결과 요약
# ============================================================
print()
print("="*70); print("완료 요약"); print("="*70)
print(f"캠페인 ID:    {CAMPAIGN_ID}")
print(f"광고그룹 ID:  {ADGROUP_ID}")
print(f"광고소재:     {len(created_ad_ids)}개")
print(f"키워드:       {len(KEYWORDS)}개")
print(f"\n광고주센터 확인: https://manage.searchad.naver.com")
print(f"비즈채널 검수 통과되면 광고그룹 status가 자동 ELIGIBLE 전환")
