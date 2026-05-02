---
name: 수정 기록 (시간순)
description: 2026-04-29 세션의 모든 변경 사항을 시간순으로 기록 — 무엇을 왜 어떻게 바꿨는지
type: project
---

# 수정 기록 — 2026-04-29

## 27. 라이브 준비 Phase 1 — 이전 사이트 트래킹 제거 + 코드 정리
**참조**: 형제 폴더 `cantaviledition.com` (Vercel 라이브 사례), `부정클릭방지시스템/`
**범위**: 82개 HTML 파일 + `gtag/` 폴더 + `board/` 129개 URL + 모바일 38개 canonical + 신규 `.gitignore` / `vercel.json`

**Why**: 이전 분양사이트 코드 그대로 복사한 상태라 GTM/Google Ads ID가 이전 사이트 계정으로 박혀 있어 새 도메인에서 그대로 라이브하면 이전 분양사 분석 데이터에 오염됨. GitHub 푸시 + Vercel 배포 전 완전 정리 필요.

### 트래킹 ID 제거 (4종 블록 perl 일괄)
- **GTM-TGHF9M29** (Google Tag Manager) — 82개 HTML 파일에서 head 블록 + body noscript iframe 모두 제거
- **AW-17370728994** (Google Ads gtag) — 동일 파일에서 gtag/js 로더 + config 블록 제거
- **gtag('event', ...)** 페이지뷰 이벤트 스크립트 제거
- **G-TNYYRLMMV8** GA4 주석 1줄 제거 (write.php.html)
- `gtag/` 폴더(js + js-1, 약 770KB) 백업 후 제거 — 참조 없는 고아 파일
- 잔여 `GA_event()` 헬퍼 함수(board/js/common.js)는 `typeof gtag == 'function'` 가드 있어 안전하게 유지 (새 GA4 ID 넣으면 자동 작동)

### 코드 정리
- 신규 `.gitignore` — `_bak_*`, `*.bak`, `node_modules`, `.env`, `.vercel/` 제외
- 신규 `vercel.json` — image/img/sub/css/js/ajax/npm/gh/s/meta/popup/mobile 정적자산 1년 immutable 캐시
- `board/` 129개 절대URL `https://sujain-roicent.co.kr/board/...` → 루트상대 `/board/...` 일괄 치환 (URL 인코딩된 형태도 같이)
- 모바일 38개 canonical `http://sujain-roicent.co.kr` → 페이지별 파일명 (예: `brand.html`)

### 백업
- [_bak_inherited_analytics_strip/](../../_bak_inherited_analytics_strip/) — 트래킹 제거 전 82개 + gtag/
- [_bak_phase1_cleanup/](../../_bak_phase1_cleanup/) — board/adm + board/bbs + mobile/*.html 107개 원본

### 다음 세션 진행 작업
[.claude/memory/07_launch_status.md](07_launch_status.md) 참조 — 새 도메인 / 마케팅 ID / 부정클릭시스템 결정 필요

## 26. PC 전화번호 1877-9896 브랜드 컬러 적용
**범위**: [css/style-1.css](../../css/style-1.css) ~ [css/style-17.css](../../css/style-17.css) (17개)

- `.call_num` base color `#393939` → `var(--m_color)` (=#00486e, 브랜드 네이비)
- `.header_open:hover .call_num` 동일 적용 (hover 상태도 브랜드컬러 유지)
- `.fp-viewing-X .call_num` 흰색 헤더 상태(`#fff`)는 그대로
- 메뉴 링크 hover(`#393939`)는 변경 없음
- perl `-0777` multiline regex로 `.call_num{...color:#393939}` 블록만 정확히 매치 (다른 `#393939` 사용처는 보존)
- 백업: [_bak_callnum_color/](../../_bak_callnum_color/) (17개 원본)

## 25. 모바일 게시판 iframe 정상화 (.php → .php.html)
**범위**: 모바일 9개 페이지 + [board/bbs/board.php.html](../../board/bbs/board.php.html)

**Why**: 모바일 페이지들이 `../board/bbs/board.php?bo_table=...` 형식으로 iframe src 잡고 있는데 실제 파일은 `.php.html` 확장자. 정적 서버에서 404 발생.

- 변경 파일: news.html, reservation01~04.html, reservation01_check~04_check.html
  - `board.php` → `board.php.html`
  - `write.php` → `write.php.html`
  - `book_conf.php` → `book_conf.php.html`
- news.html 추가 수정: `scrolling="yes"` → `scrolling="no"` (이중 스크롤 제거), `onload="resizeIframe(this)"` 미존재 함수 호출 제거. 이미 부모-자식 postMessage 기반 자동 리사이즈 시스템이 있음 (`childData` event)
- board.php.html에 `<meta name="viewport" content="width=device-width, initial-scale=1.0">` 추가 (iframe 콘텐츠 모바일 렌더 정상화)
- 백업: [_bak_iframe_php_ext/](../../_bak_iframe_php_ext/) (9개 모바일 + 1개 board 원본)

## 24. 모바일 메뉴 정리 — 사업안내 라벨 + 프리미엄 페이지 활성화
**범위**: 모바일 37개 페이지 + 신규 [mobile/premium.html](../../mobile/premium.html) + [js/device-redirect.js](../../js/device-redirect.js)

### 24-1. hea_drop 첫 항목 라벨 수정
- 모바일 페이지의 `<ul class="hea_drop">` 첫 항목이 "사업개요"로 잘못 라벨됨 (실제로는 6개 카테고리 중 첫번째 = 사업안내)
- perl로 `<ul class="hea_drop">\s*\n\s*<li><a href="planning\.html">사업개요` → `사업안내` 일괄 치환 (37개 파일)
- GNB sub 메뉴와 smenu의 "사업개요"는 그대로 유지 (실제 사업개요 서브페이지)

### 24-2. 모바일 프리미엄 페이지 신규 생성
- 기존 `<!-- <li><a href="premium.html">프리미엄</a></li> -->` 주석 처리 상태 → 활성화
- mobile/premium.html 신규 (brand.html 템플릿 기반, 헤더/GNB/smenu 동일)
- 본문: 처음엔 `mobile/img/premium/premium1~8.jpg` 8장 스택 → 사용자 요청으로 PC 동일 이미지 `../sub/bon/pc/premium.jpg` 단일 사용으로 변경
- inline `style="width:100%"` 제거 → 글로벌 `.sub_bottom img { width: calc(100% - 40px); max-width: 560px }` 자동 적용
- 모든 모바일 페이지의 GNB + smenu에서 `<!-- premium 주석 -->` 활성화 (perl 일괄)
- [js/device-redirect.js](../../js/device-redirect.js) `paired` 리스트에 `premium.html` 추가 → 자동 PC↔모바일 분기 작동

### 백업
- [_bak_hea_drop_label/](../../_bak_hea_drop_label/) — 36개 모바일 원본

## 23. 관심고객등록 폼 운정 스타일 후속 픽스 (PC + 모바일 통합)
**범위**: PC [customer.html](../../customer.html), 모바일 [mobile/customer.html](../../mobile/customer.html), 폼 [board/bbs/write.php.html](../../board/bbs/write.php.html), [board/skin/board/guest_add/style.css](../../board/skin/board/guest_add/style.css)

### 23-1. PC customer.html 폼 일련의 버그픽스
- **flatpickr CSS 누락** → `<link href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">` 추가. 기존엔 prev/next 화살표 SVG가 raw 사이즈로 떠 있었음
- **이름 입력칸 폭** — 레거시 `.user_name { width: 157px }`(line 297)가 새 운정 룰을 specificity로 이김. style.css line 914에 override `.guest_table td input.user_name { width: 100%; max-width: 480px }` 추가
- **라디오 기본 선택 해제** — `id="U_checkAgreement2_2"` "동의하지 않음"의 `checked` 속성 제거
- **체크박스 좌측 여백** — `.unit_chk { padding-left: 14px }` 추가
- **※ 정렬 어긋남** — 레거시 `.oribox ul li::before { left: -15px }` 가 새 룰을 이김. specificity 올린 새 룰 추가 (`.oribox ul li::before { left: 0; top: 6px; content: "※" }`)
- **이름 위 가로선 두 줄** — `.guest_table` 레거시 `border-top: 2px solid #222`와 `.guest_table table` 모던 `border-top: 1px solid #333` 둘 다 그어짐. 모던 룰에 `border-top: 0` 추가해 외곽선 1줄로 통일
- **iframe 높이** — 1127px → 720px (콘텐츠 700-750px 충분)

### 23-2. 모바일 customer.html iframe 깨짐 수정 + 모달 통합
- iframe src `write.php?bo_table=guest` (404) → `write.php.html?bo_table=guest` (200)
- 모바일에는 PC의 개인정보 모달 / 방문예약 flatpickr 모달 / postMessage 리스너 모두 없어서 폼 안의 "보기" / "방문예약" 버튼 무반응이었음
- PC customer.html의 모달 2종 + 스크립트 + flatpickr CSS/JS 전부 모바일 customer.html 직전 `</body>`에 복사

### 23-3. 폼 CSS 레거시 누수 차단 + 모바일 미디어쿼리 보강
- write.php.html에 `<meta name="viewport">` 추가
- style.css 모던 운정 섹션 시작부에 명시적 reset:
  - `.guest_table table tr th { background:#fff !important; height:auto !important; width:auto !important; border-right:0 !important }` (legacy 회색bg, 56px 고정 height, 180px width, 컬럼 사이 세로선 제거)
  - `input[type="text"] { line-height:normal; text-indent:0; margin-left:0 !important }` (legacy line-height:50px, text-indent:10px, margin-left:1% 누수 차단)
- 모바일 미디어쿼리: 상단 여백 60→24px, col1 30→28%, hp_fixed 90→60px, oribox/btn_confirm 좌우 padding

### 백업
- [customer.html.before-flatpickr-css.bak](../../customer.html.before-flatpickr-css.bak)
- [board/bbs/write.php.html.before-radio-fix.bak](../../board/bbs/write.php.html.before-radio-fix.bak)
- [board/skin/board/guest_add/style.css.before-name-width.bak](../../board/skin/board/guest_add/style.css.before-name-width.bak)
- [mobile/customer.html.before-form-fix.bak](../../mobile/customer.html.before-form-fix.bak)

## 1. PC ↔ 모바일 자동 분기 시스템 도입
**파일**: 신규 [js/device-redirect.js](../../js/device-redirect.js), 모든 HTML 106개에 `<script>` 삽입

- viewport 너비 768px 기준으로 PC/모바일 자동 redirect
- 페어링된 38개 페이지만 처리 (PC-only/모바일-only 페이지는 그대로)
- `index.htm` ↔ `index.html` 확장자 차이 자동 처리
- `?view=pc` / `?view=mobile` 쿼리로 강제 분기 가능 (sessionStorage 저장)
- resize/orientationchange 시 250ms 디바운스 후 재평가
- `<meta name="responsive" content="true">` 마커 페이지는 redirect 스킵

## 2. 모바일 팝업 → 오산자이 스타일로 교체
**파일**: [mobile/index.html](../../mobile/index.html) (878 → 957줄)
**참조**: 바탕화면/부정클릭방지시스템/_capi_deploy/osan-xi/index.html

- 풀스크린 검은 오버레이(opacity 0.7) + 중앙 단일 이미지
- 상단에 "팝업닫기 X" 흰색 텍스트 (text-shadow로 가독성)
- Swiper로 좌우 스와이프 (3개 팝업)
- 흰색 알약형 화살표 영역 + "1 I 3" 분수형 페이지네이션
- `@keyframes pop` 위→아래 페이드 인 애니
- 닫기: 텍스트 클릭 / 검은 배경 클릭 / 슬라이드 내부 링크 클릭은 닫지 않고 이동
- 기존 날짜 기반 노출 제어 로직 보존

**중간 변경**: "관심고객 등록하고 청약 정보 받기 →" 하단 슬라이드 업 바 추가했다가 제거 (사용자 요청)

**백업**: [mobile/index.html.before-popup.bak](../../mobile/index.html.before-popup.bak)

## 3. 모바일 헤더 스크롤 효과
**파일**: [mobile/css/header.css](../../mobile/css/header.css), [mobile/js/main.js](../../mobile/js/main.js)

- 스크롤 30px 이상 → `header.scrolled` 클래스 토글
- 흰 배경(rgba 96% 불투명) + 부드러운 그림자
- transition 0.3s ease

## 4. 모바일 로고 색상 동적 변환 (마스크 트릭)
**파일**: [mobile/css/header.css](../../mobile/css/header.css)

- 기본 흰색 로고 PNG는 그대로 사용
- 스크롤 시 PNG를 CSS 마스크로 사용 + `background-color: #004976` (브랜드 블루)
- 메뉴 오픈 시(`header.menu-open`) → 마스크 해제, 흰색 복귀
- 서브페이지(`header.is-sub`) → 마스크 적용 상시 유지

## 5. 모바일 콜 버튼 외곽선 추가
**파일**: [mobile/css/header.css](../../mobile/css/header.css)

- `header .call`에 `border: 1px solid rgba(0, 73, 118, 0.3)` 추가
- `box-sizing: border-box`로 크기 변화 방지

## 6. 서브페이지 마킹 (모바일)
**파일**: [mobile/js/main.js](../../mobile/js/main.js)

- 페이지 로드 시 `location.pathname`이 index가 아니면 `<header>`에 `is-sub` 추가
- 결과: 서브페이지에서 로고가 항상 브랜드 블루로 유지됨

## 7. 모바일 GRAND OPEN 하단 바 숨김
**파일**: [mobile/css/main.css](../../mobile/css/main.css)

- `.fix_box`에 `display: none` 추가 → 모든 모바일 페이지에 일괄 적용

## 8. 푸터 "더피알커뮤니케이션" 줄 제거
**파일**: PC 61개 + 모바일 45개 = 총 106개

- PC 패턴: `<dl><dd>온라인대행.</dd><dt>(주)더피알커뮤니케이션...</dt></dl>` (4줄 블록)
- 모바일 패턴: `<b>온라인대행.</b> (주)더피알커뮤니케이션...` (1줄)
- sed로 일괄 제거

## 9. 전화번호 일괄 변경
**범위**: 모든 HTML/CSS/JS

- `032) 875-0959` (61) → `1877-9896`
- `032-875-0959` (61) → `1877-9896`
- `032.875.0959` (45) → `1877-9896`
- 총 167개 위치 교체

## 10. PC 전화번호 표시: 이미지 → 텍스트 변환
**파일**: [css/style-1.css](../../css/style-1.css) ~ [css/style-17.css](../../css/style-17.css) (총 17개)

- 기존: `.call_num`이 `background-image: url(call_num.png)` + `text-indent: -999px`로 텍스트 숨김 후 이미지로 표시
- 변경: 텍스트 그대로 노출 (Noto Sans 18px, 700 weight)
- `.fp-viewing-X .call_num` 흰색 헤더 상태 → `color: #fff;`
- `.header_open:hover .call_num` → `color: #393939;`
- 신규 텍스트 스타일: `font-family: "Noto Sans", sans-serif; font-size: 18px; font-weight: 700; color: #393939; letter-spacing: -0.3px; line-height: 1; white-space: nowrap;`

**백업**: [_bak_subpage_callnum/](../../_bak_subpage_callnum/) (style-2 ~ style-17)
**백업**: [css/style-1.css.before-header-fix.bak](../../css/style-1.css.before-header-fix.bak)

## 11. PC FullPage 섹션 인덱스 → 헤더 색상 매핑 수정
**파일**: [css/style-1.css](../../css/style-1.css) (라인 1595~1636)

| 섹션 인덱스 | 페이지 | 변경 전 | 변경 후 |
|---|---|---|---|
| 0 | 메인비주얼 | 흰색 | 흰색 (유지) |
| 1 | LOCATION | 흰색 (오류) | 어두움 ✓ |
| 2 | UNIT | 어두움 (오류) | 흰색 ✓ |
| 3 | CONTACT | 흰색 (오류) | 어두움 ✓ |

- sed: `\.fp-viewing-1\b` → `.fp-viewing-2`
- sed: `^.fp-viewing-3\b` 라인 삭제

## 12. PC smenu HTML 평탄화 (대규모)
**파일**: PC 60개 페이지 + [_transform_smenu.py](../../_transform_smenu.py) 스크립트 작성

### Before (구조적으로 잘못된 마크업)
```html
<ul>
  <a class="home"><img></a>     <!-- 유효하지 않은 HTML -->
  <li class="smenu_depth1"><a>홈으로</a></li>
  <li class="smenu_depth1">     <!-- 7개 메뉴를 다 감싸는 wrapper -->
    <ul>
      <li><a>사업안내</a><ul class="smenu_depth2">...</ul></li>
      ...
    </ul>
  </li>
</ul>
```

### After (평탄화)
```html
<ul>
  <li class="home"><a><img></a></li>
  <li class="smenu_depth1 no_drop"><a>홈으로</a></li>  <!-- 나중에 제거됨 -->
  <li class="smenu_depth1"><a>사업안내</a><ul class="smenu_depth2">...</ul></li>
  ...
  <li class="smenu_depth1 no_drop"><a>관심고객등록</a></li>
</ul>
```

### Python 스크립트 핵심 로직
- HTML 주석 안의 `<ul>`/`<li>`까지 regex가 잡는 버그 → `skip_comment()` 함수로 해결
- depth 추적으로 wrapper 매칭 (non-greedy regex의 한계 극복)
- sub-menu가 없는 항목엔 자동으로 `no_drop` 클래스 부여

**백업**: [_bak_smenu/](../../_bak_smenu/) (60개 PC HTML)

## 13. PC smenu CSS / JS 셀렉터 평탄화 대응 업데이트
**파일**: 60개 페이지 + [css/style-1.css](../../css/style-1.css) ~ style-17.css

- JS: `$('.smenu_depth1 > ul > li')` → `$('.smenu_depth1:not(.no_drop)')`
- CSS hover: `.smenu_depth1 > ul > li:hover .smenu_depth2` → `.smenu_depth1:hover .smenu_depth2`

## 14. PC smenu에서 "홈으로" 항목 제거
**파일**: PC 60개 페이지

- 좌측 홈 아이콘과 중복 → 텍스트 "홈으로" 항목만 제거
- perl로 3줄 블록 제거

## 15. PC smenu 동적 브레드크럼 빌더
**파일**: 신규 [js/smenu-breadcrumb.js](../../js/smenu-breadcrumb.js), PC 60개 페이지의 inline JS 교체

- 페이지마다 inline `<script>`(URL 필터링 로직)를 외부 스크립트로 교체
- `[홈] | [현재 카테고리 ▼] | [현재 페이지 ▼]` 형식으로 런타임에 재구성
- 카테고리 드롭다운: 모든 카테고리 (다른 카테고리로 점프)
- 페이지 드롭다운: 같은 카테고리의 sibling sub-page들
- `normalizeUrl()` 함수로 URL 매칭 (`_check`, `notice##`, 숫자/언더바 정규화)

## 16. smenu 폭/정렬 조정
**파일**: [css/style-2.css](../../css/style-2.css) ~ style-17.css (16개)

1. `.smenu .rel_wrap`에 `max-width: 1100px; margin: 0 auto;` 추가 → 컨텐츠 영역(`.one_image_page max-width: 1100px`)과 좌측 정렬 일치
2. `.smenu ul`에 `justify-content: flex-end` 추가 → 항목들 우측 정렬

(중간 시도) `.smenu .rel_wrap`에 `justify-content: flex-end` 추가했다가 잘못된 셀렉터임을 발견하고 revert. 실제 flex 컨테이너는 `<ul>`임.

## 17. 청약안내 카테고리 완전 제거
**범위**: PC 60개 페이지의 smenu + application*.html 파일 9개

- smenu의 `<li class="smenu_depth1"><a href="application1.html">청약안내</a>...</li>` 블록 제거
- `application1.html`, `application2.html`, `application2_01~05.html`, `application3.html`, `application4.html` 파일 9개 삭제
- PC/모바일 헤더 메뉴의 청약안내는 이미 주석 처리되어 있던 상태 (그대로 유지)

**백업**: [_bak_application_pages/](../../_bak_application_pages/) (9개 파일)

## 22. 관심고객등록(customer.html) 폼 운정 아이파크 스타일로 개편
**참조**: 운정 아이파크 (`unjeong-ipark.com/bbs/write.html`)
**범위**: [board/bbs/write.php.html](../../board/bbs/write.php.html) 폼 마크업 + [board/skin/board/guest_add/style.css](../../board/skin/board/guest_add/style.css) 새 CSS 추가

**Why**: 기존 폼이 시각적으로 산만하고 거주지 3-단계 select가 사용자에게 부담. 영업적으로는 이름/전화/관심타입만 받으면 충분.

### 폼 필드 변경
| Before | After |
|---|---|
| 고객명 | 이름 (placeholder 추가, * 필수 표시) |
| 연락처 (010+숫자) | 휴대폰 (`010` select - hyphen - 4자리 - hyphen - 4자리) |
| 거주지 (시/도, 구/군, 동/면 3개 select) | **삭제** (hidden input으로만 유지하여 백엔드 호환) |
| (없음) | **관심타입** 체크박스 (84A, 84B, 84G, 84H, 101) |

### CSS (운정 스타일)
- 1100px max-width 중앙 정렬
- 회색 배경(#f3f3f3) 인풋, border 없음
- 표 형태 (col1 18% / col 82%)
- 상단 2px 검정 border, 행 사이 1px #e5e5e5
- 등록하기(검정) / 다시쓰기(흰색) 버튼 (160×50px)
- 모바일 반응형 (≤768px)

### 백엔드 호환
- `wr_name`, `hp1`, `hp2`, `hp3`는 그대로 유지 → 데이터 수집 정상
- `wr_5[]` (관심타입) 새 필드 추가 — gnuboard wr_5 컬럼에 저장됨
- `wr_6/7/8` (구거주지)은 hidden input으로 빈 값 전송 — 백엔드 변수 누락 방지

### 백업
- [_bak_event_notice/write.php.html.bak](../../_bak_event_notice/write.php.html.bak)
- [_bak_event_notice/guest_add-style.css.bak](../../_bak_event_notice/guest_add-style.css.bak)

## 21. 언론보도(news.html) 카드 그리드 레이아웃 변환
**참조**: 김포 칸타빌 에디션 (`cantaviledition.com/ver01/theme/basic/skin/board/press_new/style.css`)
**범위**: 단일 파일 [board/skin/board/news_add/style.css](../../board/skin/board/news_add/style.css) (PC + 모바일 동시 적용)

**Why**: 기존 단순 리스트(제목+설명 한 줄씩) → 칸타빌 스타일 카드 그리드로 시각적 풍요로움 확보. board.php가 iframe으로 PC/모바일 양쪽에서 로드되므로 skin CSS 한 곳만 수정하면 양쪽 동시 적용.

### 동작
- **데스크톱(≥1100px)**: 4-column 그리드, 카드당 ~25% 폭
- **태블릿(768~1100px)**: 3-column
- **모바일(≤768px)**: 2-column
- **작은 모바일(≤480px)**: 1-column

### 카드 구성
- 출처 라벨: `js_tit > span` (브랜드 블루 #004976, 작은 글씨)
- 제목: `js_tit` (16px, bold, 2-line clamp)
- 설명: `js_con` (13px, 회색, 3-line clamp)
- hover 시 테두리 #004976 + 그림자 효과

### 백업
[_bak_event_notice/news_add-style.css.bak](../../_bak_event_notice/news_add-style.css.bak)

## 20. 홍보센터 메뉴 축소 (이벤트/공지사항 제거) + 하단 여백 축소
**범위**: PC 50+개 + 모바일 44개 페이지 + 12개 파일 삭제 + CSS 16개 조정

**Why**: 영업/홍보 단계 정리 — 이벤트와 공지사항 카테고리 더 이상 운영 안 함. 하단 여백이 과도하다는 사용자 피드백.

### 메뉴 변경
```
[Before] 홍보센터 → 언론보도, 홍보영상, 이벤트, 공지사항
[After]  홍보센터 → 언론보도, 홍보영상
```

### 처리 패턴
1. **이벤트 li 제거** — `<li><a href="event_open.html">이벤트</a></li>` (PC/모바일 모든 메뉴 위치)
2. **공지사항 li 제거** — `<li><a href="notice.html">공지사항</a></li>` (PC/모바일 모든 메뉴 위치)
3. **모바일 sub-page smenu_wrap의 multi-line li**도 처리 (sm_event_open 등 다중 클래스 가진 a 태그 포함)

### 파일 삭제 (12개)
- PC: `event_open.html`, `event_open2.html`, `event_open3.html`, `event_open4.html`, `event_a_02.html`, `notice.html`
- 모바일: `mobile/event.html`, `mobile/event_open.html`, `mobile/event_open2.html`, `mobile/event_open3.html`, `mobile/event_open4.html`, `mobile/notice.html`

### 후속 정리
- [js/device-redirect.js](../../js/device-redirect.js) `paired` 리스트에서 `event_open*.html`, `notice.html` 제거

### 하단 여백 축소 (시도 → 사용자 요청으로 원복)
- 처음 `.smenu { margin-bottom: 200px → 80px }`로 줄임
- 사용자 추가 요청으로 30px까지 줄였으나, 결과 마음에 들지 않아 200px(원본)로 다시 복원
- `footer.sub_footer { margin-top: 100px }`도 원본 유지

### 결정 메모
**Why 원복**: 디자인적으로 sub_visual의 인하대 hero 영역(400px) 다음에 적정한 호흡이 필요. 30px / 80px로 압축하면 페이지가 답답해 보임. 사용자 시각적 판단이 200px가 옳다고 결론.

**How to apply**: 향후 페이지 여백 조정 시 .smenu margin-bottom은 200px 유지. 다른 부분(sub_visual 자체 height, footer top 등)을 먼저 조정 검토.

### 백업
[_bak_event_notice/](../../_bak_event_notice/) — 12개 파일 백업

## 19. 메뉴 통합: 계약안내 → 분양안내 + notice02 삭제
**범위**: PC 50+개 + 모바일 44개 페이지 + notice02 파일 2개

**Why**: 영업 단계 단순화 — 계약안내 카테고리를 별도로 유지할 필요가 없어짐. 분양 관련 모든 정보를 한 카테고리로 묶음. "추가 선택품목 계약 안내문"은 더 이상 노출 불필요.

### 새 메뉴 구조
```
[Before]
  분양안내 → 공급안내
  계약안내 → 계약체결 안내, 자금조달 계획서, 인지세 안내문, 추가 선택품목 계약 안내문

[After]
  분양안내 → 공급안내, 계약체결 안내, 자금조달 계획서, 인지세 안내
```

### 처리한 패턴 (Python 스크립트 [_merge_menus.py](../../_merge_menus.py))
1. **PC `header_menu_wrap`** — 분양안내 li + 계약안내 li → 통합된 분양안내 li (50개)
2. **PC `smenu`** — 동일 패턴, smenu_depth1 클래스 (50개)
3. **모바일 `gnb`** — 분양안내 + 계약안내 `<span>` li → 통합 (1개, mobile/index.html)
4. **모바일 서브페이지 `hea_drop`** — `<li><a href="contract.html">계약안내</a></li>` 제거 (41개)
5. **모바일 서브페이지 `<!-- 분양안내 -->` smenu_wrap** — 새 4개 항목으로 교체 (41개)
6. **모바일 서브페이지 `<!-- 계약안내 -->` smenu_wrap** — 블록 통째로 제거 (41개)
7. **`<h2>계약안내</h2>` 페이지 타이틀 → `<h2>분양안내</h2>`** (12개 — contract, document_capital, stampduty, notice02, reservation01-04 + _check)
8. **`gtag('event', '계약안내', ...)` 분석 이벤트** — 그대로 유지 (GA 데이터 연속성)

### 파일 삭제
- `notice02.html` (PC)
- `mobile/notice02.html`

### 후속 정리
- [js/device-redirect.js](../../js/device-redirect.js) `paired` 리스트에서 `notice02.html` 제거
- 잔여 검증: 모든 활성 메뉴에서 `계약안내` 카테고리 0개, `notice02` 참조 0개

### 백업
[_bak_menu_merge/](../../_bak_menu_merge/) — 영향받은 97개 파일 + notice02 파일 2개

### 알려진 미정리 항목
- `document_common*.html` (서류제출안내 6개 페이지) — 더 이상 활성 메뉴에 연결 안 됨 → 사실상 orphan. 사용자 판단에 따라 별도 삭제 가능.

## 18. 오시는길(contact) 페이지 완전 제거
**범위**: PC 52개 + 모바일 45개 = 97개 페이지의 모든 contact.html 링크 + 파일 2개

**Why**: 영업 정책 — 고객이 모델하우스에 방문 전 반드시 관심고객등록 또는 전화 상담을 거치도록 함. 위치 정보 노출 차단.

- 두 가지 링크 패턴 모두 제거:
  - `<li><a href="contact.html">오시는길</a></li>` (헤더 메뉴, smenu)
  - `<li><a href="contact.html" class="sm_contact">오시는길</a></li>` (sm 변형)
- 파일 삭제: `contact.html`, `mobile/contact.html`
- [js/device-redirect.js](../../js/device-redirect.js)의 `paired` 리스트에서 `contact.html` 제거 → 자동 redirect 대상에서 제외
- 잔여 검증: 전체 프로젝트에서 `contact.html` 참조 0개

**백업**: [_bak_contact_pages/](../../_bak_contact_pages/) (PC + 모바일 파일 2개)
