---
name: 파일 맵 + 백업 위치
description: 신규/수정 파일 목록, 백업 폴더 위치, 복원 명령어 — 작업 영향 범위 추적용
type: reference
---

# 파일 맵 (수정 영향 범위 + 백업 매핑)

## 신규 작성 파일

| 경로 | 역할 | 비고 |
|---|---|---|
| [js/device-redirect.js](../../js/device-redirect.js) | viewport 기반 PC↔모바일 자동 분기 | 모든 HTML 106개에 `<script>` 삽입됨 |
| [js/smenu-breadcrumb.js](../../js/smenu-breadcrumb.js) | PC 서브페이지 동적 브레드크럼 빌더 | PC 60개 페이지에서 로드됨 |
| [_transform_smenu.py](../../_transform_smenu.py) | smenu 평탄화 변환 스크립트 (1회성) | 재실행 가능, 보존 권장 |
| [CLAUDE.md](../../CLAUDE.md) | 프로젝트 컨텍스트 (Claude Code 자동 로드) | 항상 최신 상태 유지 |
| `.claude/settings.json` | 프로젝트 설정 (권한 등) | |
| `.claude/memory/*.md` | 본 메모리 파일들 | |

## 수정된 파일 (요약)

### CSS (총 17개)
| 파일 | 주요 변경 |
|---|---|
| [css/style-1.css](../../css/style-1.css) | `.fp-viewing-X` 매핑 수정, `.call_num` 텍스트화, `.smenu_depth1:hover` 셀렉터 |
| [css/style-2.css](../../css/style-2.css) ~ [css/style-17.css](../../css/style-17.css) | `.call_num` 텍스트화, `.smenu_depth1:hover`, `.smenu .rel_wrap` max-width:1100px, `.smenu ul` justify-end |
| [mobile/css/header.css](../../mobile/css/header.css) | `header.scrolled`, `header.menu-open`, `header.is-sub`, 콜 버튼 border, 로고 마스크 트릭 |
| [mobile/css/main.css](../../mobile/css/main.css) | `.fix_box { display: none; }` 추가 |

### HTML (총 106개)
- **PC root**: 51개 `*.html` + `index.htm` 모두 수정 (전화번호, 푸터, smenu, device-redirect 스크립트)
- **mobile/**: 45개 모두 수정 (전화번호, 푸터, device-redirect 스크립트)
- **PC 60개**는 추가로 smenu 평탄화 + breadcrumb JS 적용

### JS
| 파일 | 변경 |
|---|---|
| [mobile/js/main.js](../../mobile/js/main.js) | scroll → `header.scrolled` 토글, menu open → `header.menu-open` 토글, sub-page 감지 → `header.is-sub` 추가 |

## 삭제된 파일

| 파일 | 백업 위치 |
|---|---|
| `application1.html` | [_bak_application_pages/application1.html.bak](../../_bak_application_pages/) |
| `application2.html` | 동일 폴더 |
| `application2_01.html` ~ `application2_05.html` | 동일 폴더 |
| `application3.html`, `application4.html` | 동일 폴더 |

## 백업 폴더 (모두 프로젝트 루트)

| 폴더 | 보관 내용 | 복원 명령 |
|---|---|---|
| [_bak_smenu/](../../_bak_smenu/) | smenu 평탄화 전 PC HTML 60개 | `cp _bak_smenu/<name>.bak <name>` |
| [_bak_subpage_callnum/](../../_bak_subpage_callnum/) | 전화번호 텍스트화 전 style-2~17.css | `cp _bak_subpage_callnum/<name>.bak css/<name>` |
| [_bak_application_pages/](../../_bak_application_pages/) | 삭제된 청약안내 9개 HTML | `cp _bak_application_pages/<name>.bak <name>` |

## 단일 파일 백업 (프로젝트 루트)

| 백업 파일 | 원본 | 복원 명령 |
|---|---|---|
| `index.htm.before-merge.bak` | [index.htm](../../index.htm) | `mv index.htm.before-merge.bak index.htm` |
| `mobile/index.html.before-popup.bak` | [mobile/index.html](../../mobile/index.html) | `mv mobile/index.html.before-popup.bak mobile/index.html` |
| `css/style-1.css.before-header-fix.bak` | [css/style-1.css](../../css/style-1.css) | `mv css/style-1.css.before-header-fix.bak css/style-1.css` |

## 영향 받지 않은 영역 (기존 그대로)
- `image/` — 모든 이미지 그대로
- `popup/` — 팝업 이미지 그대로
- `meta/`, `pdf/`, `gtag/`, `gh/`, `ajax/`, `npm/` — 외부 자산 그대로
- `mobile/img/` — 모바일 이미지 그대로
- `js/jquery-3.6.0.min.js`, `js/common.js`, `js/main.js`, `js/tab.js` — 기존 PC JS 그대로
- `css/reset.css`, `css/common.css`, `css/common-N.css`, `css/style.css` — 미수정
- `mobile/css/reset.css`, `mobile/css/common.css`, `mobile/css/sub.css`, `mobile/css/slick.css`, `mobile/css/swiper.min.css` — 미수정
- `mobile/js/*` (main.js 외) — 미수정

## 전체 복원 (Nuclear Option)
모든 변경을 되돌리려면 백업 폴더들에서 순차적으로 복원하면 됨. 단, 신규 파일(`js/device-redirect.js`, `js/smenu-breadcrumb.js`, `_transform_smenu.py`)은 `rm` 필요.
