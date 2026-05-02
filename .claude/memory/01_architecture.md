---
name: 사이트 아키텍처 (PC/모바일 분리 구조)
description: PC와 모바일이 완전히 별개 마크업/CSS로 운영되는 이중 구조 + 자동 분기 메커니즘 상세
type: project
---

# 사이트 아키텍처

## 핵심 사실: PC와 모바일은 완전히 별개 사이트
- **마크업 다름**: PC `index.htm`(2200줄+) vs 모바일 `mobile/index.html`(950줄+) — 같은 콘텐츠라도 HTML 구조 자체가 다름
- **CSS 다름**: PC는 `css/style-N.css`, 모바일은 `mobile/css/*.css`
- **JS 다름**: PC는 FullPage.js 기반 1-section 1-page 스크롤, 모바일은 일반 스크롤
- **공유 자산만 같음**: 이미지 폴더(`image/`, `popup/`), 메타(`meta/`), gtag

## 자동 분기 (device-redirect.js)
- viewport ≤ 768px → `/mobile/<page>` 로 redirect
- viewport > 768px → 루트 `/<page>` 로 redirect
- 페어링된 페이지 38개만 redirect (양쪽에 모두 존재하는 파일)
- `?view=pc` 또는 `?view=mobile` 쿼리 → sessionStorage에 저장하여 강제 분기 무시
- `<meta name="responsive" content="true">` 마커가 있는 페이지는 redirect 스킵
- resize/orientationchange 이벤트에서 250ms 디바운스 후 재평가

### 페어 매핑
- `index.htm` (PC) ↔ `index.html` (모바일) — 확장자 다름 주의
- 그 외 38개는 동일 파일명

### 스킵 페이지 (한쪽만 존재)
- PC 전용: `pr.html`, `pr2.html`, `pr3.html`, `premium.html`, `schedule.html`, `event_a_02.html`, `document_common*.html`
- 모바일 전용: `event.html`, `movie.html`, `reservation04.html`, `reservation04_check.html`

## PC index.htm 구조
- FullPage.js로 5개 섹션 (인덱스 0~4):
  - **0**: 메인비주얼 (어두운 배경) → 헤더 흰색
  - **1**: LOCATION (밝은 배경) → 헤더 어두움
  - **2**: UNIT Plan (어두운 파랑) → 헤더 흰색
  - **3**: CONTACT US (밝은 배경) → 헤더 어두움
  - **4**: footer
- 헤더 색상: `body.fp-viewing-X` 클래스 기반 CSS 분기
  - `style-1.css:1595`~ : `.fp-viewing-0, .fp-viewing-2`에서 흰색 헤더

## PC 서브페이지 (style-2 ~ style-17 사용)
각 페이지는 `header_top` (메인 헤더) + `smenu` (브레드크럼) 두 영역으로 구성:
1. **header_top**: 풀 메뉴 (모든 카테고리), 모든 페이지 공통
2. **smenu**: 페이지별 브레드크럼
   - `js/smenu-breadcrumb.js`가 런타임에 동적으로 재구성
   - 결과: `[홈 아이콘] | [현재 카테고리 ▼] | [현재 페이지 ▼]`

### smenu HTML 구조 (평탄화 후)
```html
<div class="smenu">
  <div class="rel_wrap">  <!-- max-width: 1100px, margin: 0 auto -->
    <ul>  <!-- display: flex, justify-content: flex-end -->
      <li class="home"><a href="index.htm"><img></a></li>
      <li class="smenu_depth1"><a>카테고리</a><ul class="smenu_depth2">...</ul></li>
      <li class="smenu_depth1"><a>현재 페이지</a><ul class="smenu_depth2">...</ul></li>
    </ul>
  </div>
</div>
```

## 모바일 헤더 구조
- `<header>` 안에 햄버거 버튼 + 콜 버튼 + 로고 + nav
- 스크롤 30px 이상 → `header.scrolled` 클래스 추가 (흰 배경 + 그림자)
- 메뉴 열림 → `header.menu-open` 클래스 (배경 투명, 로고 흰색 복원)
- 서브페이지 → `header.is-sub` 클래스 (로고 항상 브랜드 블루)

### 로고 색상 변환 트릭
PNG 마스크로 흰 로고를 브랜드 블루로 동적 변환:
```css
header.scrolled h1, header.is-sub h1 {
  background-image: none;
  background-color: #004976;
  -webkit-mask-image: url("../img/logo.png");
}
```

## 색상 토큰
- 브랜드 블루: `#004976` (= `#00486E` 변종, 실제 사용)
- CSS variable: `--m_color: #00486e` (style-1.css:4 등)
- 헤더 텍스트: `#393939` (어두운 회색)

## 폰트
- PC: Noto Sans, Nanum Myeongjo, NanumBarunGothic
- 모바일: Pretendard
