"""
수자인 SEO 2차 보강 (2026-05-07 야간)

Google 공식 가이드 검토 결과 기반 작업:
1. mobile/reservation04.html, _check.html title 13자 → 페이지 의도 명시
2. description <80자 75건 중 단지정보 활용해 120~160자로 확장 (페이지별 차별화)
3. twitter:card 4종 메타 추가 (twitter:card / title / description / image)

원칙:
- 본문/스타일/스크립트 미변경 (head 메타만)
- og:title/og:description도 동일하게 동기화
- mobile은 PC 정본을 alt로 두므로 description은 PC와 동일 (canonical로 묶임)
- idempotent: 이미 보강된 항목 skip
"""
import glob, os, re

# 페이지별 길고 차별화된 description (PC 기준, mobile은 동일하게 적용)
DESC_MAP = {
    'index.htm': '인천 미추홀구 용현·학익 2-2블록 인하대역 1구역 도시정비사업. 지하2층~지상43층 6개동 총 1,199세대 매머드 단지(임대 240/일반분양 959). GTX-B 인천청학역 확정, 인하대 도보권. 입주 2029년 4월.',
    'brand.html': '명품 주거 브랜드 수자인. 한신공영의 노하우와 입주민 라이프스타일에 맞춘 프리미엄 주거 가치를 인하대역 로이센트로 새롭게 제안합니다. 1,199세대 매머드 단지에서 누리는 수자인의 품격.',
    'community.html': '키즈룸·시니어센터·피트니스·도서관·게스트하우스 등 1,199세대 매머드 단지에 어울리는 풀스펙 커뮤니티. 전 세대가 함께 누리는 입주민 전용 공간으로 일상의 품격을 높이는 수자인 로이센트.',
    'complex.html': '6개 동 최적 배치로 채광·통풍·조망 극대화. 풍부한 조경 공간과 입주민 동선을 고려한 단지 설계. 지하2층~지상43층 1,199세대(임대 240/일반분양 959) 인하대역 1구역 매머드 단지의 배치도.',
    'contract.html': '인하대역 수자인 로이센트 분양계약 절차, 필요 서류, 계약금/중도금/잔금 납부 일정 안내. 1차 계약금 1,000만원 등 합리적 자금 부담으로 시작하는 내 집 마련 가이드.',
    'customer.html': '인하대역 수자인 로이센트 관심고객등록·견본주택 방문예약. 사전 등록 시 분양 정보 우선 안내와 한정 사은품 제공. 인천 용현·학익 1,199세대 매머드 단지 분양 정보를 가장 먼저 받아보세요.',
    'document_capital.html': '주택청약 자금조달 계획서 작성 가이드. 항목별 입력 방법과 필요 서류, 제출 시 유의사항을 인하대역 수자인 로이센트 청약·계약 안내와 함께 한눈에 정리.',
    'document_common.html': '주택분양 계약 시 필요한 공통 서류 안내. 신분증·인감·주민등록등본 등 준비물과 발급 방법, 제출 절차를 인하대역 수자인 로이센트 계약자에게 명확히 안내합니다.',
    'document_common_01.html': '인하대역 수자인 로이센트 특별공급 서류제출안내(1편). 신혼부부·생애최초·다자녀·노부모 등 특별공급 유형별 필요 서류와 작성 방법을 정리한 청약 준비 가이드.',
    'document_common_02.html': '인하대역 수자인 로이센트 특별공급 서류제출안내(2편). 자격 입증 서류, 가점·우선순위 산정 자료 등 청약 신청자가 직접 챙겨야 할 핵심 항목을 단계별로 안내합니다.',
    'document_common_03.html': '인하대역 수자인 로이센트 특별공급 서류제출안내(3편). 소득·자산·무주택 기간 등 검증 항목별 발급기관과 제출 양식을 인하대역 수자인 로이센트 청약자 기준으로 정리.',
    'document_common_04.html': '인하대역 수자인 로이센트 특별공급 서류제출안내(4편). 추가 제출 서류, 보완 요청 시 대응 방법, 마감 후 절차 등 청약 막바지에 자주 묻는 항목을 모았습니다.',
    'document_common_05.html': '인하대역 수자인 로이센트 특별공급 서류제출안내(5편). 최종 제출 체크리스트와 누락 시 불이익, 모델하우스 현장 접수 안내까지 청약 마무리 단계 종합 가이드.',
    'interior.html': '수자인 로이센트의 모던하고 세련된 인테리어 컨셉과 마감 디테일. 평형별 공간 구성과 프리미엄 자재 사양으로 일상의 격을 높이는 인하대역 수자인 로이센트 인테리어.',
    'item_list.html': '주택 옵션, 빌트인 가전, 시스템 가구 등 인하대역 수자인 로이센트의 전시품목과 옵션 사양 안내. 평형별 기본 제공 항목과 추가 선택 옵션을 한눈에 비교할 수 있도록 정리.',
    'location.html': '인하대역 초역세권, GTX-B 인천청학역(확정) 수혜. 용현초·인항고·인하대 학세권. 인천공항·제2경인고속도로·KTX 광역 교통망. 인천 미추홀구 용현·학익 2-2블록 핵심 입지.',
    'magam.html': '평형별 바닥재·벽지·주방·욕실 마감재 리스트. 친환경 자재와 프리미엄 사양 적용. 인하대역 수자인 로이센트 84A/84B/84G/84H/101 5개 주택형의 마감 사양을 한 자리에서 확인.',
    'magam-1.html': '인하대역 수자인 로이센트 전용 84A·84B Type 마감재 리스트. 거실·침실·주방·욕실·현관 부위별 자재와 시공 사양을 평형 단위로 상세히 안내합니다.',
    'magam-2.html': '인하대역 수자인 로이센트 전용 84G·84H Type 마감재 리스트. 거실·침실·주방·욕실·현관 부위별 자재와 시공 사양을 평형 단위로 상세히 안내합니다.',
    'magam-3.html': '인하대역 수자인 로이센트 전용 101 Type(펜트하우스급) 마감재 리스트. 거실·침실·주방·욕실·현관 부위별 자재와 프리미엄 사양을 한눈에 확인할 수 있도록 정리.',
    'news.html': '인하대역 수자인 로이센트 관련 최신 언론보도와 분양 소식. GTX-B 호재, 청약 일정, 모델하우스 오픈 등 주요 이슈를 모아둔 인하대역 수자인 로이센트 뉴스 센터.',
    'planning.html': '인천 미추홀구 용현동 604-7번지 일원, 지하2층~지상최고43층 6개동 총 1,199세대(임대 240 포함). 일반분양 959세대(특별공급 445 포함). 입주 2029년 4월 예정 사업 개요.',
    'pr.html': '인하대역 수자인 로이센트 홍보영상 1편. 입지·단지·커뮤니티의 핵심 가치를 영상으로 만나는 공식 홍보 콘텐츠. 인천 용현·학익 1,199세대 매머드 단지 소개.',
    'pr2.html': '인하대역 수자인 로이센트 홍보영상 2편. 평형별 평면과 인테리어 컨셉, 입주민 라이프스타일을 담은 공식 홍보 콘텐츠로 단지의 매력을 입체적으로 전달합니다.',
    'pr3.html': '인하대역 수자인 로이센트 홍보영상 3편. 모델하우스·교통 호재·청약 안내까지 분양 검토에 필요한 핵심 정보를 영상으로 압축한 공식 홍보 콘텐츠.',
    'premium.html': '용현·학익 최중심 입지, 1,199세대 매머드 단지, 6억대 합리적 가격, 1차 계약금 1,000만원, 견본주택 방문 사은품 등 인하대역 수자인 로이센트의 7대 프리미엄 한눈에 보기.',
    'reservation01.html': '인하대역 수자인 로이센트 서류접수 방문예약. 원하는 날짜와 시간을 선택해 견본주택 서류 제출 일정을 사전 예약하세요. 대기 없이 빠르게 안내받을 수 있습니다.',
    'reservation01_check.html': '인하대역 수자인 로이센트 서류접수 방문예약 확인·취소. 예약 내역 조회와 일정 변경, 취소까지 한 화면에서 처리. 견본주택 방문 전 예약 상태를 미리 확인하세요.',
    'reservation02.html': '인하대역 수자인 로이센트 예비 당첨자 서류접수 방문예약. 예비 순위 안내에 따라 견본주택 방문 일정을 사전 예약하고, 필요 서류를 미리 준비하실 수 있습니다.',
    'reservation02_check.html': '인하대역 수자인 로이센트 예비 당첨자 서류접수 방문예약 확인·취소. 예약 내역 조회와 일정 변경, 취소를 한 화면에서 처리. 견본주택 방문 전 상태를 점검하세요.',
    'reservation03.html': '인하대역 수자인 로이센트 정당계약 방문예약. 분양 당첨자 정당계약 일정 사전 예약. 원하는 날짜와 시간을 선택해 계약 절차를 신속하게 진행하실 수 있습니다.',
    'reservation03_check.html': '인하대역 수자인 로이센트 정당계약 방문예약 확인·취소. 예약 내역 조회와 일정 변경, 취소를 한 화면에서 처리. 계약 방문 전 예약 상태를 미리 확인하세요.',
    'schedule.html': '인하대역 수자인 로이센트 분양 일정 안내. 청약 접수, 당첨자 발표, 계약 체결, 입주(2029년 4월) 등 단계별 일정을 한눈에 확인할 수 있도록 정리한 공식 캘린더.',
    'stampduty.html': '주택 분양계약 인지세 산정 방법과 납부 안내. 분양가별 인지세액, 전자수입인지 구매 절차를 인하대역 수자인 로이센트 계약자 기준으로 쉽게 정리한 가이드.',
    'supply.html': '인하대역 수자인 로이센트 공급안내. 총 1,199세대(임대 240 포함) 중 일반분양 959세대(특별공급 445 포함) 평형별 세대수와 공급 면적을 한 표에서 확인.',
    'system.html': '스마트홈, 공기정화 시스템, 단열·방음, 에너지 절감 등 수자인 로이센트의 첨단 주거 시스템. 입주민 일상의 편의와 건강을 위해 단지 전체에 적용된 기술 사양을 안내합니다.',
    'unit.html': '전용 84A/84B/84G/84H/101 5종 주택형. 일반분양 959세대. 평형별 평면도와 세대수를 한 페이지에서 비교. 인하대역 수자인 로이센트 주택형 전체 안내.',
    'unit-1.html': '인하대역 수자인 로이센트 전용 84A 208세대(공급 117.29㎡)·84B 513세대(공급 116.46㎡) 평면도와 면적·세대 정보. 4베이 판상형 위주의 인기 주력 평형 상세 안내.',
    'unit-2.html': '인하대역 수자인 로이센트 전용 84G 43세대(공급 117.63㎡)·84H 25세대(공급 117.03㎡) 평면도와 면적·세대 정보. 차별화된 평면 구성의 희소 평형 상세 안내.',
    'unit-3.html': '인하대역 수자인 로이센트 전용 101㎡ 170세대(공급 139.74㎡) 평면도와 면적·세대 정보. 펜트하우스급 광폭 평형의 거실·침실·주방 동선 구성을 상세히 안내.',
    'vr.html': '인하대역 수자인 로이센트 평형별 360도 VR 사이버 모델하우스. 견본주택을 온라인으로 미리 체험하고 거실·주방·침실 동선을 입체적으로 확인하실 수 있습니다.',
    'vr-1.html': '인하대역 수자인 로이센트 전용 84A·84B Type 360도 VR 모델하우스. 4베이 판상형 주력 평형의 거실·주방·침실·욕실을 온라인에서 입체적으로 체험.',
    'vr-2.html': '인하대역 수자인 로이센트 전용 84G·84H Type 360도 VR 모델하우스. 차별화 평면의 거실·주방·침실·욕실을 온라인에서 입체적으로 체험할 수 있습니다.',
    'vr-3.html': '인하대역 수자인 로이센트 전용 101 Type 360도 VR 모델하우스. 펜트하우스급 광폭 평형의 거실·주방·침실·욕실을 온라인에서 입체적으로 체험할 수 있습니다.',
}

# mobile/reservation04 title 보강 (root는 vercel.json rewrite로 customer.html, mobile은 실파일)
TITLE_OVERRIDE = {
    'mobile/reservation04.html': '관심고객등록 (방문예약) | 인하대역 수자인 로이센트',
    'mobile/reservation04_check.html': '관심고객등록 확인·취소 | 인하대역 수자인 로이센트',
}
DESC_MAP['mobile/reservation04.html'] = '인하대역 수자인 로이센트 관심고객등록·방문예약. 견본주택 사전 예약 시 분양 정보 우선 안내와 한정 사은품 제공. 모바일에서 빠르게 등록하실 수 있습니다.'
DESC_MAP['mobile/reservation04_check.html'] = '인하대역 수자인 로이센트 관심고객등록 확인·취소. 등록 내역 조회와 변경·취소를 한 화면에서 처리. 견본주택 방문 전 예약 상태를 미리 확인하세요.'
# 모바일 메인은 basename(index.html)이 PC(index.htm)와 다르므로 별도 매핑
DESC_MAP['index.html'] = DESC_MAP['index.htm']
# 모바일 movie.html은 PC 페이지가 없는 모바일 전용 — 홍보영상
DESC_MAP['movie.html'] = '인하대역 수자인 로이센트 홍보영상 모음. 입지·단지·평형·커뮤니티 등 분양 검토에 필요한 핵심 정보를 영상으로 한 번에 확인할 수 있는 모바일 전용 페이지.'

TWITTER_BLOCK = '''  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://sujainroicent.com/meta/og_share.jpg">
'''

def get_pc_basename(path):
    """mobile/foo.html → foo.html (DESC_MAP 조회용)"""
    base = os.path.basename(path)
    # mobile/reservation04 같은 mobile 전용 키는 그대로 path 사용
    if path.replace('\\', '/') in DESC_MAP:
        return path.replace('\\', '/')
    return base

def patch_file(path):
    c = open(path, encoding='utf-8').read()
    orig = c
    changes = []

    pkey = path.replace('\\', '/')

    # 1. title override
    if pkey in TITLE_OVERRIDE:
        new_title = TITLE_OVERRIDE[pkey]
        m = re.search(r'<title>([^<]+)</title>', c)
        if m and m.group(1) != new_title:
            c = c.replace(m.group(0), f'<title>{new_title}</title>', 1)
            changes.append(f'title: {m.group(1)} → {new_title}')
        # og:title도 동기화
        m2 = re.search(r'(<meta\s+property="og:title"\s+content=")([^"]+)(")', c)
        if m2 and m2.group(2) != new_title:
            c = c.replace(m2.group(0), m2.group(1) + new_title + m2.group(3), 1)
            changes.append('og:title sync')

    # 2. description 보강
    desc_key = get_pc_basename(path) if pkey not in DESC_MAP else pkey
    if desc_key in DESC_MAP:
        new_desc = DESC_MAP[desc_key]
        m = re.search(r'(<meta\s+name="description"\s+content=")([^"]+)(")', c)
        if m and m.group(2) != new_desc:
            c = c.replace(m.group(0), m.group(1) + new_desc + m.group(3), 1)
            changes.append(f'description ({len(m.group(2))}자→{len(new_desc)}자)')
        # og:description도 동기화
        m2 = re.search(r'(<meta\s+property="og:description"\s+content=")([^"]+)(")', c)
        if m2 and m2.group(2) != new_desc:
            c = c.replace(m2.group(0), m2.group(1) + new_desc + m2.group(3), 1)
            changes.append('og:description sync')

    # 3. twitter:card 추가 (없을 때만)
    if 'twitter:card' not in c:
        # 현재 title/desc 기준으로 채움
        t_m = re.search(r'<title>([^<]+)</title>', c)
        d_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
        title_v = t_m.group(1) if t_m else '인하대역 수자인 로이센트'
        desc_v = d_m.group(1) if d_m else ''
        # og:image 메타 이후에 삽입 (또는 og:image:alt 이후)
        block = TWITTER_BLOCK.format(title=title_v, desc=desc_v)
        # og:image:alt 다음 줄에 삽입 시도, 없으면 og:image 다음
        target = re.search(r'(<meta\s+property="og:image:alt"\s+content="[^"]+"\s*/?>)', c)
        if not target:
            target = re.search(r'(<meta\s+property="og:image"\s+content="[^"]+"\s*/?>)', c)
        if target:
            c = c.replace(target.group(1), target.group(1) + '\n' + block.rstrip(), 1)
            changes.append('twitter:card 4종 추가')

    if c != orig:
        open(path, 'w', encoding='utf-8').write(c)
        return changes
    return None


def main():
    files = sorted(glob.glob('*.htm') + glob.glob('*.html') + glob.glob('mobile/*.htm') + glob.glob('mobile/*.html'))
    files = [f for f in files if not (
        '_bak_' in f or '.bak' in f or 'before-popup' in f or 'before-sec06' in f or 'before-flatpickr' in f
    )]

    total, modified = 0, 0
    for path in files:
        total += 1
        result = patch_file(path)
        if result:
            modified += 1
            print(f'[{path}]')
            for ch in result:
                print(f'  - {ch}')

    print(f'\n=== 총 {total}개 검사, {modified}개 수정 ===')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
