---
name: 주요 의사결정 근거
description: 작업 중 내린 핵심 디자인/아키텍처 결정과 그 이유 — 미래 대안 탐색 시 참고
type: project
---

# 주요 의사결정 근거

## 결정 1: PC와 모바일 통합 반응형 변환은 포기, 자동 분기 방식 채택

**상황**: 사용자가 처음에 "PC와 모바일을 하나의 반응형 사이트로 합쳐달라"고 요청

**시도한 옵션**
- A안: PC 마크업과 모바일 마크업을 같은 HTML에 wrap한 후 미디어쿼리로 토글
- B안: iframe 기반 wrapper

**결과**: A안으로 `index.htm` 표본 작업 → CSS cascade 충돌(`body`, `.gnb` 등 공유 선택자)로 디자인 깨짐 → 사용자가 롤백 요청

**최종 결정**: 자동 분기 (device-redirect.js) + 기존 마크업 보존

**Why**: 
- PC와 모바일이 처음부터 별개 디자인으로 설계됨 → 사후 통합은 비현실적
- 미디어쿼리만으로 정합성 보장 불가
- 진짜 반응형은 디자인 시스템부터 새로 만들어야 함 (수일~수주 작업)

**How to apply**: 향후 "통합" 요청이 와도 같은 함정에 빠지지 않도록 — 처음부터 백업 강조하고 표본 1개만 시도해서 보여줄 것. 일괄 60+개 변환은 비추.

---

## 결정 2: smenu 평탄화는 Python depth-tracking 스크립트로 처리

**상황**: 60개 PC 페이지의 smenu가 invalid HTML + 잘못된 nesting 구조

**시도한 옵션**
- sed/perl 단순 정규식 → 비활성 주석 안의 `<ul>`/`<li>`를 잡아서 depth 어긋남
- non-greedy regex → 잘못된 `</ul></li>` 페어 매칭 (가장 가까운 close에 매칭됨)

**최종 결정**: [_transform_smenu.py](../../_transform_smenu.py) — Python으로 depth tracking + HTML 주석 스킵

**Why**:
- HTML이 dirty (주석 안에 태그 잔재) → regex로는 안전하게 처리 불가
- 60개 일괄 처리 → 실수 시 복구 비용 큼 → 검증된 스크립트 필요

**How to apply**: 향후 HTML 구조 변경 작업도 비슷한 패턴 → Python 스크립트 + 백업 폴더 + 검증 단계 분리.

---

## 결정 3: PC smenu 동적 브레드크럼 → 외부 JS 파일

**상황**: 페이지마다 `currentUrl = normalizeUrl("planning.html")` 하드코딩된 inline 스크립트

**시도한 옵션**
- 각 페이지의 inline 스크립트를 다 다르게 수정
- 단일 외부 JS 파일이 `window.location`을 읽고 동적 처리

**최종 결정**: [js/smenu-breadcrumb.js](../../js/smenu-breadcrumb.js) 외부 파일

**Why**:
- 1개 파일 수정으로 60개 페이지 동작 변경 가능 → 유지보수 용이
- inline JS 60개를 모두 동기화하는 것보다 안정적
- 향후 브레드크럼 동작 변경도 1곳만 수정

**How to apply**: 페이지 간 공유 로직은 항상 외부 JS로. inline은 페이지-특화 로직만.

---

## 결정 4: PC 전화번호 이미지 → 텍스트 변환

**상황**: `.call_num`이 `background-image: url(call_num.png)` + `text-indent: -999px`로 텍스트를 숨기고 이미지로 표시 → 전화번호 변경 시 이미지 새로 만들어야 함

**최종 결정**: 17개 style 파일 모두에서 텍스트 기반으로 변환 (Noto Sans 18px 700 weight)

**Why**:
- 전화번호 변경 빈도 높음 (이미 `032 → 1877-9896` 변경 작업 발생)
- 이미지보다 텍스트가 SEO/접근성에서 우월
- CSS만 변경하면 됨 (HTML은 이미 텍스트 포함)

**How to apply**: 다른 이미지로 텍스트 표현된 요소도 동일하게 텍스트화 권장.

---

## 결정 5: device-redirect.js의 `<meta name="responsive">` 마커

**상황**: 만약 미래에 어떤 페이지를 진짜 반응형으로 만들면, device-redirect가 거기서 또 redirect를 발생시켜 무한 루프 위험

**최종 결정**: `<meta name="responsive" content="true">` 마커가 있으면 redirect 스킵

**Why**:
- 향후 점진적 반응형 마이그레이션 가능성 대비
- 현재는 어떤 페이지도 이 마커를 가지지 않음 (다 분리 운영)

**How to apply**: 향후 어떤 페이지를 반응형으로 통합할 때 `<head>`에 반드시 이 메타 태그 추가.

---

## 결정 6: smenu 평탄화 시 `no_drop` 클래스 자동 부여

**상황**: sub-menu가 없는 항목(홈으로, 관심고객등록)에 화살표 아이콘이 표시되면 안됨

**최종 결정**: Python 스크립트가 `<ul class="smenu_depth2">`가 없는 top-level `<li>`에 자동으로 `class="smenu_depth1 no_drop"` 부여

**Why**:
- 기존 CSS의 `.smenu_depth1.no_drop:after { transform: ... !important }` 룰 활용
- 수동으로 페이지마다 클래스 부여하는 것보다 자동화가 안정적

**How to apply**: 향후 sub-menu가 추가/삭제되면 다시 스크립트 돌리면 됨.

---

## 결정 7: 모바일 로고 색상은 PNG 마스크 트릭

**상황**: 흰색 PNG 로고밖에 없는데, 스크롤/서브페이지에선 어두운 배경에 잘 안 보임 → 색상 있는 로고 PNG 새로 만들기 vs CSS 트릭

**최종 결정**: PNG를 CSS `mask-image`로 사용 + `background-color`로 색 채우기

**Why**:
- 새 이미지 파일 생성 불필요
- 색상 변경은 CSS `background-color` 한 줄로 가능
- 모든 모던 브라우저(Safari, Chrome, Firefox, Edge) 지원

**How to apply**: 다른 단색 PNG 아이콘도 동일 트릭 적용 가능.
