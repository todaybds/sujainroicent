# 인하대역 수자인 로이센트 — 프로젝트 컨텍스트

이 파일은 Claude Code가 이 프로젝트에서 작업할 때 자동으로 읽는 메인 컨텍스트입니다.
세부 내용은 [.claude/memory/](.claude/memory/)를 참조하세요.

---

## 프로젝트 개요
- **유형**: 정적 HTML 부동산 분양 사이트 (인하대역 수자인 로이센트)
- **기술 스택**: 정적 HTML/CSS/JS, jQuery 3.6, Swiper 11, Slick, GSAP, FullPage.js
- **빌드 시스템 없음**: 파일을 직접 수정하면 바로 반영됨
- **Git 미사용**: 모든 수정 전 반드시 백업 폴더에 사본 보관

## 사이트 구조
- **PC 버전**: 프로젝트 루트의 `*.html` / `*.htm` 파일들
- **모바일 버전**: `mobile/` 폴더 안의 동일 파일들
- **공유 자산**: `image/`, `popup/`, `css/`, `js/`, `meta/`, `pdf/`, `gtag/`, `gh/`, `ajax/`, `npm/`
- **자동 분기**: `js/device-redirect.js`가 viewport 768px 기준으로 PC ↔ 모바일 자동 redirect (페어링된 페이지 한정)

## 핵심 엔트리포인트
- PC 메인: [index.htm](index.htm) — FullPage.js 기반, 5개 섹션 (intro/location/unit/contact/footer)
- 모바일 메인: [mobile/index.html](mobile/index.html) — 일반 스크롤 구조

## 커스텀 스크립트 (직접 작성)
1. [js/device-redirect.js](js/device-redirect.js) — viewport 기반 PC ↔ 모바일 자동 분기
2. [js/smenu-breadcrumb.js](js/smenu-breadcrumb.js) — PC 서브페이지 동적 브레드크럼 빌더
3. [_transform_smenu.py](_transform_smenu.py) — smenu HTML 평탄화 변환 스크립트 (1회성, 보존)

## 백업 폴더 (모두 이전 작업의 안전 복원용)
- `_bak_smenu/` — smenu 평탄화 전 PC HTML 60개
- `_bak_subpage_callnum/` — 전화번호 텍스트화 전 style-2 ~ style-17
- `_bak_application_pages/` — 삭제된 청약안내 페이지 9개
- `index.htm.before-merge.bak`, `mobile/index.html.before-popup.bak` 등 단일 파일 백업
- `css/style-1.css.before-header-fix.bak`

## 반드시 지킬 규칙
1. **Git이 없으므로 수정 전 항상 백업 폴더 만들기** (`_bak_*` 패턴)
2. **PC와 모바일은 마크업이 완전히 다름** — 한쪽 수정이 다른 쪽에 영향 없음
3. **CSS는 17개 style-N.css로 페이지마다 다름** — 일괄 수정 시 모든 파일 동기화
4. **HTML 주석 안에 `<ul>`/`<li>`가 들어있는 경우** 종종 있음 → depth 추적 시 반드시 주석 스킵
5. **device-redirect.js 무한 redirect 방지**: 통합된 페이지엔 `<meta name="responsive" content="true">` 마커 필요

## 메모리 인덱스 (자세한 정보)
- [.claude/memory/01_architecture.md](.claude/memory/01_architecture.md) — 사이트 구조 상세
- [.claude/memory/02_modifications_log.md](.claude/memory/02_modifications_log.md) — 시간순 수정 기록
- [.claude/memory/03_design_decisions.md](.claude/memory/03_design_decisions.md) — 주요 의사결정 근거
- [.claude/memory/04_file_map.md](.claude/memory/04_file_map.md) — 파일 위치 + 백업 매핑
- [.claude/memory/05_conventions.md](.claude/memory/05_conventions.md) — 작업 패턴 / 회피 사항
- [.claude/memory/06_known_issues.md](.claude/memory/06_known_issues.md) — 알려진 이슈
- [.claude/memory/07_launch_status.md](.claude/memory/07_launch_status.md) — **라이브 준비 진행상태 (Phase 1 완료, 2/3 대기)** ⭐ 다음 세션은 여기부터
