---
name: 알려진 이슈 / 한계
description: 현재 알려진 이슈와 의도적으로 그대로 둔 부분 — 사용자가 다시 물을 수 있는 항목들
type: project
---

# 알려진 이슈 및 의도적 한계

## 1. URL 정규화 (`-1`, `-2` 변형) — 해결 완료 (2026-04-29)
[js/smenu-breadcrumb.js](../../js/smenu-breadcrumb.js)의 `normalizeUrl()`에 다음 라인 추가:
```js
url = url.replace(/-\d+(?=\.|$)/g, '');  // magam-1 → magam, vr-2 → vr 등
```
영향: `magam-1/2/3.html`, `unit-1/2/3.html`, `vr-1/2/3.html`이 각각 부모 카테고리(magam/unit/vr)와 정상 매칭되어 brewd­crumb 표시됨.

## 2. 청약안내 직접 URL 접근 시 404
- application*.html 파일 9개 삭제됨
- 기존에 검색엔진/북마크에 인덱싱된 URL 있을 수 있음 → 404 발생
- **해결 방향**: 서버 단에서 application*.html → index.htm 또는 supply.html로 301 redirect 설정 (정적 호스팅이라면 _redirects 또는 .htaccess 필요)

## 3. PC 메인 (index.htm)은 smenu 평탄화 작업 영향 안 받음
- index.htm은 smenu가 없음 (FullPage.js 풀페이지 구조)
- 평탄화 작업은 서브페이지 60개에만 적용됨
- style-1.css의 `.smenu_*` 룰은 dead code일 수 있음 (확인 필요)

## 4. include/smenu.css 와 include/stab.css는 사용 안 됨
- HTML이 `class="smenu"`를 쓰는데 [include/smenu.css](../../include/smenu.css)는 `.smenu_wrap` 셀렉터를 씀 → 매칭되는 요소 없음
- 이 두 파일은 dead code일 가능성 큼
- **결정**: 안전을 위해 파일은 그대로 둠 (실제 영향 없음)

## 5. PC 헤더 메뉴는 모든 페이지 공통
- `header_menu_wrap`은 60개 PC 페이지 모두 동일한 7개 카테고리 노출
- smenu만 페이지별로 동적 브레드크럼 (smenu-breadcrumb.js)
- 헤더 메뉴는 hover 드롭다운으로 sub-page 노출

## 6. 모바일 팝업의 날짜 설정
[mobile/index.html](../../mobile/index.html)의 팝업 노출 기간:
- p1 (popup37-1.jpg): 2021-11-01 ~ 2099-07-04 → 활성
- p2 (popup33-1.jpg): 2026-03-11 ~ 2099-12-15 → 활성
- p3 (popup29-1.jpg): 2021-11-01 ~ 2099-12-15 → 활성

날짜 만료 시 자동으로 팝업 제거됨. 새 팝업 추가 시 같은 패턴으로 li 추가 + ranges 배열에 push.

## 7. device-redirect.js의 Resize 동작
- 창 크기를 768px 경계 너머로 드래그하면 자동으로 PC ↔ 모바일 리다이렉트
- **부작용**: 폼 입력 도중 의도치 않게 페이지 이동 가능
- **해결 옵션**: `RESIZE_DEBOUNCE_MS`를 250 → 800+ 으로 조정하거나, 폼 페이지에서 비활성화

## 8. 모바일 사이트에 `<meta name="responsive">` 없음
- 모바일 페이지는 PC viewport에서 redirect 대상 (PC로 이동)
- 모바일 페이지를 의도적으로 PC에서 보고 싶으면 `?view=mobile` 쿼리 사용

## 9. PC 인트로 애니메이션
- `index.htm`에 GSAP 기반 인트로 애니메이션 있음 (skip 버튼 마우스 따라옴)
- FullPage.js와 함께 동작
- 미디어 분기 작업 시 망가지면 복구 가능 ([index.htm.before-merge.bak](../../index.htm.before-merge.bak))
