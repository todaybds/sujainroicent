"""칸타빌 캠페인의 광고그룹/광고소재 패턴 GET (페이로드 형식 학습용)"""
import hmac, hashlib, base64, time, json, requests

CUSTOMER_ID = "2553973"
API_KEY = "0100000000c702d5195228f5a8beab47a4f7764f89bacdd13c238b0b5a1417de7837f15150"
SECRET_KEY = "AQAAAADHAtUZUij1qL6rR6T3dk+JwFv9rwXHelEXd+997wTIXg=="
BASE_URL = "https://api.searchad.naver.com"

def sig(ts,m,uri):
    return base64.b64encode(hmac.new(SECRET_KEY.encode(),f"{ts}.{m}.{uri}".encode(),hashlib.sha256).digest()).decode()
def req(method,uri,params=None):
    ts=str(int(time.time()*1000))
    h={"X-Timestamp":ts,"X-API-KEY":API_KEY,"X-Customer":CUSTOMER_ID,"X-Signature":sig(ts,method,uri),"Content-Type":"application/json; charset=UTF-8"}
    url=BASE_URL+uri
    r=requests.get(url,headers=h,params=params,timeout=30) if method=="GET" else requests.post(url,headers=h,json=params,timeout=30)
    if r.status_code!=200:
        print(f"  HTTP {r.status_code}: {r.text[:300]}")
        return None
    return r.json()

CAMPAIGN_KANTAVIL = "cmp-a001-01-000000010296459"

print("[광고그룹 목록 — 칸타빌]")
ag = req("GET","/ncc/adgroups",params={"nccCampaignId":CAMPAIGN_KANTAVIL})
brand_core_id = None
if ag:
    for a in ag:
        nm = a.get('name')
        aid = a.get('nccAdgroupId')
        bid = a.get('bidAmt')
        print(f"  {aid}  '{nm}'  bid={bid}  status={a.get('status')}")
        if '브랜드' in str(nm) or '핵심' in str(nm):
            brand_core_id = aid

if brand_core_id:
    print(f"\n[광고그룹 디테일 — '브랜드 핵심' {brand_core_id}]")
    d = req("GET",f"/ncc/adgroups/{brand_core_id}")
    if d:
        print(json.dumps(d,ensure_ascii=False,indent=2)[:2000])

    print(f"\n[광고소재 목록 — 광고그룹 {brand_core_id}]")
    ads = req("GET","/ncc/ads",params={"nccAdgroupId":brand_core_id})
    if ads:
        for a in ads[:2]:
            print(json.dumps(a,ensure_ascii=False,indent=2)[:1500])
            print("---")
